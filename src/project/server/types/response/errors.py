from dataclasses import dataclass

from project.server.types.request import YttgRequest
from project.server.types.response.base import LinkError, ProviderError, YttgError
from project.server.types.response.enums import ResponseStatus, YttgErrorMessage


@dataclass(frozen=True, slots=True)
class UnmatchedRequestError(YttgError):
    request: YttgRequest
    """Request that has not been matched."""

    def __init__(self, request: YttgRequest) -> None:
        object.__setattr__(self, 'status', ResponseStatus.INTERNAL_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.UNMATCHED_REQUEST)
        object.__setattr__(self, 'request', request)


@dataclass(frozen=True, slots=True)
class IllFormedLinkError(LinkError):
    """Not a valid YouTube link."""

    def __init__(self, link: str) -> None:
        object.__setattr__(self, 'status', ResponseStatus.CLIENT_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.ILL_FORMED_LINK)
        object.__setattr__(self, 'link', link)


@dataclass(frozen=True, slots=True)
class NoResultFoundError(LinkError):
    """A valid YouTube link that does not correspond to any video."""

    def __init__(self, link: str) -> None:
        object.__setattr__(self, 'status', ResponseStatus.CLIENT_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.NO_RESULT_FOUND)
        object.__setattr__(self, 'link', link)


@dataclass(frozen=True, slots=True)
class NotSubscribedError(ProviderError):
    """Telegram user not subscribed to channels required by the provider."""

    def __init__(self, provider: str) -> None:
        object.__setattr__(self, 'status', ResponseStatus.TELEGRAM_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.NOT_SUBSCRIBED_ERROR)
        object.__setattr__(self, 'provider', provider)


@dataclass(frozen=True, slots=True)
class InvalidChannelHashError(YttgError):
    channel: str
    """Tag of an invalid channel."""

    def __init__(self, channel: str) -> None:
        object.__setattr__(self, 'status', ResponseStatus.TELEGRAM_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.INVALID_CHANNEL_HASH)
        object.__setattr__(self, 'channel', channel)


@dataclass(frozen=True, slots=True)
class InvalidLanguageError(YttgError):
    language: str
    """Chosen YouTube video language."""

    def __init__(self, language: str) -> None:
        object.__setattr__(self, 'status', ResponseStatus.CLIENT_ERROR)
        object.__setattr__(self, 'message', YttgErrorMessage.INVALID_LANGUAGE)
        object.__setattr__(self, 'language', language)
