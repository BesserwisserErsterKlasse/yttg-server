from dataclasses import dataclass
from typing import Any

from pyrogram.client import Client as PyrogramClient
from pyrogram.handlers.handler import Handler

from modules.telegram.handler.add import add_handler
from modules.telegram.handler.remove import remove_handler


@dataclass(frozen=True, slots=True)
class TempHandler[HandlerT: Handler]:
    """Add a temporary handler to a Pyrogram client."""

    client: PyrogramClient
    handler: HandlerT
    group: int

    async def __aenter__(self) -> None:
        await add_handler(self.client, self.handler, self.group)

    async def __aexit__(self, *_: Any) -> None:
        await remove_handler(self.client, self.handler, self.group)
