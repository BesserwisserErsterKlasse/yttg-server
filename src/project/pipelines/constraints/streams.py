from itertools import chain

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message as PyrogramMessage

from modules.telegram.constraint import constraint
from project.pipelines.utils import parse_stream


@constraint
def has_streams(message: PyrogramMessage) -> bool:
    """If the message has the stream menu."""

    if not isinstance(message.reply_markup, InlineKeyboardMarkup):
        return False
    for button in chain(*message.reply_markup.inline_keyboard):
        try:
            parse_stream(button.text)
        except AssertionError:
            return False
    return True
