from dataclasses import dataclass

from project.server.types.request import YttgRequest
from project.server.types.response.base import YttgError
from project.server.types.response.enums import ResponseStatus, YttgErrorMessage


class InternalError(YttgError, status=ResponseStatus.INTERNAL_ERROR):
    pass


@dataclass(frozen=True, slots=True)
class UnmatchedRequestError(InternalError, message=YttgErrorMessage.UNMATCHED_REQUEST):
    """Request has no corresponding registered handler."""

    request: YttgRequest
    """Request that has not been matched."""
