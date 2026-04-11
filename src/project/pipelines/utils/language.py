from copy import deepcopy

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message as PyrogramMessage


def parse_language(text: str) -> str | None:
    """Parse language from flag."""

    flag: str = text.strip()[0:2]
    code: int = (ord(flag[0]) << 16) | ord(flag[1])
    return {
        8353870311: 'en',
        8354787832: 'en',
        8353477114: 'en',
        8353608170: 'de',
        8353477113: 'de',
        8353608173: 'fr',
        8353739255: 'fr',
        8353477098: 'ar',
        8353608166: 'fr',
        8353739256: 'es',
        8354263549: 'es',
        8353477111: 'pt',
        8354001401: 'it',
        8354394617: 'pt',
        8354263537: 'nl',
        8354656746: 'sv',
        8354263540: 'no',
        8353608176: 'da',
        8353739246: 'fi',
        8354394609: 'pl',
        8353608191: 'cs',
        8354656752: 'sk',
        8353870330: 'hu',
        8354525684: 'ro',
        8353477100: 'bg',
        8353870327: 'el',
        8354787814: 'uk',
        8354525690: 'ru',
        8354656759: 'tr',
        8354656742: 'ar',
        8353739244: 'ar',
        8354001393: 'he',
        8354001395: 'hi',
        8353608179: 'zh',
        8354656764: 'zh',
        8354001397: 'ja',
        8354132471: 'ko',
        8354656749: 'th',
        8354787827: 'vi',
        8354001385: 'id',
        8354263550: 'ms',
        8354001399: 'fa',
        8353739242: 'et',
        8354132475: 'lv',
        8354132473: 'lt',
    }.get(code)


def parse_languages(message: PyrogramMessage) -> dict[str, tuple[int, int]]:
    """Parse languages supported by a given YouTube video stream."""

    assert isinstance(message.reply_markup, InlineKeyboardMarkup)
    return {
        langcode: deepcopy((x, y))
        for x, button_row in enumerate(message.reply_markup.inline_keyboard)
        for y, button in enumerate(button_row)
        if (langcode := parse_language(button.text)) is not None
    }
