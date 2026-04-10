from copy import deepcopy
from re import compile, Match, Pattern
from typing import Final

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message as PyrogramMessage

from project.server.types import Stream

STREAM_KIND: Final[Pattern[str]] = compile(pattern=fr'(?P<stream>{r'|'.join(Stream)})')


def parse_stream(text: str) -> Stream:
    m: Match[str] | None = STREAM_KIND.search(text)
    assert m is not None and m.group('stream') is not None
    return Stream(m.group('stream'))


def parse_streams(message: PyrogramMessage) -> dict[Stream, tuple[int, int]]:
    """Parse YouTube video streams."""

    assert isinstance(message.reply_markup, InlineKeyboardMarkup)
    return {
        parse_stream(button.text): deepcopy((x, y))
        for x, button_row in enumerate(message.reply_markup.inline_keyboard)
        for y, button in enumerate(button_row)
    }
