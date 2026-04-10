from abc import ABC
from dataclasses import dataclass

from project.server.types.response.enums import ResponseStatus, YttgErrorMessage


@dataclass(frozen=True, slots=True)
class YttgResponse(ABC):
    status: ResponseStatus
    """Response status."""


@dataclass(frozen=True, slots=True)
class YttgError(YttgResponse, ABC):
    message: YttgErrorMessage
    """Response error message."""


@dataclass(frozen=True, slots=True)
class LinkError(YttgError, ABC):
    link: str
    """Link to the YouTube video."""


@dataclass(frozen=True, slots=True)
class ProviderError(YttgError):
    provider: str
    """Tag of the telegram bot that handles the request."""
