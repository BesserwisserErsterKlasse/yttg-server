from itertools import chain

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message as PyrogramMessage

from modules.telegram.constraint import constraint
from project.pipelines.utils import parse_language


@constraint
def has_languages(message: PyrogramMessage) -> bool:
    """If the message has the language menu."""

    if not isinstance(message.reply_markup, InlineKeyboardMarkup):
        return False
    for button in chain(*message.reply_markup.inline_keyboard):
        assert isinstance(button.callback_data, str)
        if not button.callback_data.startswith('youtube_back'):
            if parse_language(button.text) is None:
                return False
    return True
