from asyncio import Event, PriorityQueue
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import override

from pyrogram.client import Client as PyrogramClient
from pyrogram.enums import ParseMode
from pyrogram.filters import bot, private
from pyrogram.handlers.edited_message_handler import EditedMessageHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message as PyrogramMessage

from modules.telegram import Proxy, TelegramDriver
from modules.telegram.handler import add_handler
from project.telegram.chat import AcquiredChat, OrderedMessage


@dataclass(slots=True)
class YttgDriver(TelegramDriver):
    __chat_acquisition_events: dict[str, Event]
    __message_queues: dict[str, PriorityQueue[OrderedMessage]]

    @override
    async def start(self) -> None:
        await super(YttgDriver, self).start()
        await add_handler(
            client=self._client,
            handler=MessageHandler(self.__on_message, bot & private),
            group=0,
        )
        await add_handler(
            client=self._client,
            handler=EditedMessageHandler(self.__on_message, bot & private),
            group=0,
        )

    def acquire(self, chat_id: str) -> AcquiredChat:
        """Acquire exclusive chat ownership."""

        if chat_id not in self.__chat_acquisition_events:
            self.__chat_acquisition_events[chat_id] = Event()
            self.__chat_acquisition_events[chat_id].set()
        if chat_id not in self.__message_queues:
            self.__message_queues[chat_id] = PriorityQueue()
        return AcquiredChat(
            chat_acquisition_event=self.__chat_acquisition_events[chat_id],
            message_queue=self.__message_queues[chat_id],
            send_text_callback=self.__send_text(chat_id),
            subscribe_callback=self.__subscribe(),
        )

    def __init__(
        self,
        name: str,
        api_id: int,
        api_hash: str,
        app_version: str,
        lang_code: str,
        ipv6: bool,
        proxy: Proxy | None,
        workers: int,
        workdir: Path,
        parse_mode: ParseMode,
        sleep_threshold: int,
        hide_password: bool,
        max_concurrent_transmissions: int,
    ) -> None:
        super(YttgDriver, self).__init__(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            app_version=app_version,
            lang_code=lang_code,
            ipv6=ipv6,
            proxy=proxy,
            workers=workers,
            workdir=workdir,
            parse_mode=parse_mode,
            sleep_threshold=sleep_threshold,
            hide_password=hide_password,
            max_concurrent_transmissions=max_concurrent_transmissions,
        )
        self.__chat_acquisition_events = {}
        self.__message_queues = {}

    async def __on_message(self, _: PyrogramClient, message: PyrogramMessage) -> None:
        chat_id: str = f'@{message.from_user.username}'
        if chat_id in self.__message_queues:
            self.__message_queues[chat_id].put_nowait(OrderedMessage(message))

    def __send_text(self, chat: str) -> Callable[[str], Awaitable[None]]:
        async def send_text(text: str) -> None:
            await self._client.send_message(chat_id=chat, text=text)

        return send_text

    def __subscribe(self) -> Callable[[str], Awaitable[None]]:
        async def subscribe(channel: str) -> None:
            await self._client.join_chat(chat_id=channel)

        return subscribe
