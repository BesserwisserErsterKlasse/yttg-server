from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pyrogram.types import Message as PyrogramMessage


@dataclass(frozen=True, slots=True)
class MessageConstraint:
    """Conposable message constraint."""

    func: Callable[[PyrogramMessage], bool]
    """Original constraining function."""

    def __and__(self, other: MessageConstraint) -> MessageConstraint:
        return MessageConstraint(
            lambda message: self.func(message) & other.func(message)
        )

    def __or__(self, other: MessageConstraint) -> MessageConstraint:
        return MessageConstraint(
            lambda message: self.func(message) | other.func(message)
        )

    def __xor__(self, other: MessageConstraint) -> MessageConstraint:
        return MessageConstraint(
            lambda message: self.func(message) ^ other.func(message)
        )

    def __invert__(self) -> MessageConstraint:
        return MessageConstraint(lambda message: not self.func(message))

    def __call__(self, message: PyrogramMessage) -> bool:
        return self.func(message)
