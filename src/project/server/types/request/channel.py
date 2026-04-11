from dataclasses import dataclass

from project.server.types.request.base import ProviderRequest
from project.server.types.request.enums import YttgCommand


@dataclass(frozen=True)
class ChannelInfoRequest(ProviderRequest, command=YttgCommand.GET_CHANNELS):
    pass


@dataclass(frozen=True)
class SubscribeRequest(ProviderRequest, command=YttgCommand.SUBSCRIBE):
    channels: list[str]
    """Tags of Telegram channels to subscribe to."""
