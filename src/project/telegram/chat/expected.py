from typing import NamedTuple

from modules.telegram.constraint import MessageConstraint


class ExpectedMessage[NameT: str](NamedTuple):
    """A message the bot is expected to send next."""

    constraint: MessageConstraint
    """Constraint incomming message must satisfy."""

    name: NameT
    """Name of the message."""
