from dataclasses import dataclass

from pyrogram.types import Message as PyrogramMessage


@dataclass(frozen=True, slots=True)
class OrderedMessage:
    pyrogram_message: PyrogramMessage

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, OrderedMessage):
            return NotImplemented
        return self.pyrogram_message.id < other.pyrogram_message.id
