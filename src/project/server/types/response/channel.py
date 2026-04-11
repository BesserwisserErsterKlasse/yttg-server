from dataclasses import dataclass

from project.server.types.response.base import YttgResponse
from project.server.types.response.enums import ResponseStatus


@dataclass(frozen=True, slots=True)
class ChannelInfoResponse(YttgResponse):
    channels: list[str]
    """
    Tags of Telegram channels user has to subscribe to
    in order to use the prodiver.
    """

    def __init__(self, channels: list[str]) -> None:
        object.__setattr__(self, 'status', ResponseStatus.SUCCESS)
        object.__setattr__(self, 'channels', channels)


@dataclass(frozen=True, slots=True)
class SubscribeResponse(YttgResponse):
    channels: list[str]
    """Tags of Telegram channels user subscribed to."""

    def __init__(self, channels: list[str]) -> None:
        object.__setattr__(self, 'status', ResponseStatus.SUCCESS)
        object.__setattr__(self, 'channels', channels)
