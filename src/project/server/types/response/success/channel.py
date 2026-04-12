from dataclasses import dataclass

from project.server.types.response.base import YttgSuccess


@dataclass(frozen=True, slots=True)
class ChannelInfoResponse(YttgSuccess):
    channels: list[str]
    """
    Tags of Telegram channels user has to subscribe to
    in order to use the prodiver.
    """


@dataclass(frozen=True, slots=True)
class SubscribeResponse(YttgSuccess):
    channels: list[str]
    """Tags of Telegram channels user subscribed to."""
