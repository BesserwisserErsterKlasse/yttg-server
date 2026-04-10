from typing import Literal

from pyrogram.types import Message as PyrogramMessage

from modules.telegram.constraint import constraint


@constraint
def any_message(_: PyrogramMessage) -> Literal[True]:
    """Any message passes."""

    return True


@constraint
def audio(message: PyrogramMessage) -> bool:
    """Whether the message type is audio."""

    return message.audio is not None


@constraint
def photo(message: PyrogramMessage) -> bool:
    """Whether the message type is photo."""

    return message.photo is not None


@constraint
def text(message: PyrogramMessage) -> bool:
    """Whether the message type is text."""

    return message.text is not None


@constraint
def video(message: PyrogramMessage) -> bool:
    """Whether the message type is video."""

    return message.video is not None
