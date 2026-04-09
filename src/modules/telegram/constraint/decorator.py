from collections.abc import Callable

from pyrogram.types import Message as PyrogramMessage

from modules.telegram.constraint.constaint import MessageConstraint


def constraint(func: Callable[[PyrogramMessage], bool]) -> MessageConstraint:
    """Make composable message constraint from a given function.

    >>> @constraint
    ... def photo(message: Message) -> bool:
    ...     return message.photo is not None
    ...
    >>> @constraint
    ... def caption(message: Message) -> bool:
    ...     return message.caption is not None
    ...
    >>> photo_without_caption: MessageConstraint = photo & ~caption
    """

    return MessageConstraint(func)
