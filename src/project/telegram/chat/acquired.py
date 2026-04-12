from asyncio import Event, PriorityQueue
from asyncio import sleep as asleep
from asyncio import wait_for
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Self

from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Message as PyrogramMessage

from project.telegram.chat.expected import ExpectedMessage
from project.telegram.chat.ordered import OrderedMessage
from project.telegram.retry import retry


@dataclass(slots=True)
class AcquiredChat:
    __chat_acquisition_event: Event
    __message_queue: PriorityQueue[OrderedMessage]
    __messages: dict[str, PyrogramMessage]
    __send_text_callback: Callable[[str], Awaitable[None]]
    __subscribe_callback: Callable[[str], Awaitable[None]]

    async def wait_for[NameT: str](
        self,
        *expected_messages: ExpectedMessage[NameT],
        timeout: float = 30.0,
        delay: float | None = 1.0,
    ) -> NameT:
        """
        Wait for one of the expected Telegram messages
        which matches the corresponding constraint.
        Messages that match none of the constraints are ignored.

        :param ExpectedMessage expected_messages:
            Any number of messages the bot is expected to send next.
        :param float timeout:
            Maximum time in seconds to wait for a matching message.
        :param float | None delay:
            Delay in seconds before the message is returned.
        :return str:
            Name of the first incoming message which satisfies any of the constraints.
        :raise RuntimeError:
            If `wait_for` is called before `send_text`.
        :raise TimeoutError:
            If no message satisfying the constraint has arrived in `timeout` seconds.
        """

        try:
            name, message = await wait_for(
                self.__wait_for_message(*expected_messages),
                timeout=timeout,
            )
            self.__messages[name] = message
            return name
        except TimeoutError as error:
            raise TimeoutError(
                f'No message satisfying any constraint has arrived in {timeout} seconds'
            ) from error
        finally:
            if delay is not None:
                await asleep(delay)

    async def send_text(self, text: str) -> None:
        """Send a text message to the acquired chat."""

        await self.__send_text_callback(text)

    @retry
    async def click(self, message_name: str, selector: tuple[int, int]) -> None:
        """Trigger a click on a selected button within a specified message."""

        with suppress(TimeoutError):
            await self.__messages[message_name].click(*selector, timeout=3)

    async def subscribe(self, channel_tag: str) -> None:
        """Subscribe to a specified Telegram channel."""

        with suppress(UserAlreadyParticipant):
            await self.__subscribe_callback(channel_tag)

    def __init__(
        self,
        chat_acquisition_event: Event,
        message_queue: PriorityQueue[OrderedMessage],
        send_text_callback: Callable[[str], Awaitable[None]],
        subscribe_callback: Callable[[str], Awaitable[None]],
    ) -> None:
        self.__chat_acquisition_event = chat_acquisition_event
        self.__message_queue = message_queue
        self.__messages = {}
        self.__send_text_callback = send_text_callback
        self.__subscribe_callback = subscribe_callback
        while not self.__message_queue.empty():
            self.__message_queue.get_nowait()

    def __getitem__(self, name: str, /) -> PyrogramMessage:
        return self.__messages[name]

    async def __aenter__(self) -> Self:
        await self.__chat_acquisition_event.wait()
        self.__chat_acquisition_event.clear()
        return self

    async def __aexit__(self, *_: Any) -> None:
        self.__chat_acquisition_event.set()

    async def __wait_for_message[NameT: str](
        self, *expected_messages: ExpectedMessage[NameT]
    ) -> tuple[NameT, PyrogramMessage]:
        while True:
            message: OrderedMessage = await self.__message_queue.get()
            for constraint, name in expected_messages:
                if constraint(message.pyrogram_message):
                    return name, message.pyrogram_message
            else:
                self.__message_queue.put_nowait(message)
                await asleep(delay=0.5)
