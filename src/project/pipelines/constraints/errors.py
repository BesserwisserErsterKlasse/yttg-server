from pyrogram.types import Message as PyrogramMessage

from modules.telegram.constraint import constraint


@constraint
def no_result_found_error(message: PyrogramMessage) -> bool:
    """Video is not available or does not exist."""

    return message.text is not None and 'no results found' in message.text.lower()


@constraint
def ill_formed_link_error(message: PyrogramMessage) -> bool:
    """Invalid link has been passed."""

    return message.text is not None and message.text.strip().startswith('❗️')
