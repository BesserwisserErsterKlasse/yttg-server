from asyncio import sleep as asleep

from pyrogram.client import Client as PyrogramClient
from pyrogram.handlers.handler import Handler


async def add_handler(client: PyrogramClient, handler: Handler, group: int) -> None:
    """Wait for a new handler to be added."""

    client.add_handler(handler, group=group)
    while handler not in client.dispatcher.groups.get(group, []):
        await asleep(delay=0)
