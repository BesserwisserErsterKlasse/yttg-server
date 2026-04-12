from dataclasses import dataclass

from project.server.types.response.base import YttgError
from project.server.types.response.enums import ResponseStatus, YttgErrorMessage
from project.server.types.response.errors.mixins import ProviderErrorMixin


class TelegramError(YttgError, status=ResponseStatus.TELEGRAM_ERROR):
    pass


@dataclass(frozen=True, slots=True)
class NotSubscribedError(
    ProviderErrorMixin, TelegramError, message=YttgErrorMessage.NOT_SUBSCRIBED_ERROR
):
    """Telegram user not subscribed to channels required by the provider."""

    pass


@dataclass(frozen=True, slots=True)
class InvalidChannelHashError(
    TelegramError, message=YttgErrorMessage.INVALID_CHANNEL_HASH
):
    """Channel hash is invalid."""

    channel: str
    """Tag of an invalid channel."""
