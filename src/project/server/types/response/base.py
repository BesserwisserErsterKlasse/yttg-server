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
