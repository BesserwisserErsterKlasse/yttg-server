from itertools import chain
from re import compile, Match, Pattern
from typing import Final

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message as PyrogramMessage

CHANNEL: Final[Pattern[str]] = compile(r'https?://t\.me/(?P<tag>\+?[A-Za-z0-9_]+)')


def parse_channel(text: str) -> str | None:
    """Parse channel tag from url."""

    m: Match[str] | None = CHANNEL.match(text)
    return m.group('tag') if m is not None else None


def parse_channels(message: PyrogramMessage) -> list[str]:
    """Parse channel tags."""

    assert isinstance(message.reply_markup, InlineKeyboardMarkup)
    return [
        channel
        for button in chain(*message.reply_markup.inline_keyboard)
        if button.url is not None and (channel := parse_channel(button.url)) is not None
    ]
