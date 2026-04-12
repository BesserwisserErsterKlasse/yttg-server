from dataclasses import dataclass

from project.server.types.response.base import YttgError
from project.server.types.response.enums import ResponseStatus, YttgErrorMessage
from project.server.types.response.errors.mixins import LinkErrorMixin


class ClientError(YttgError, status=ResponseStatus.CLIENT_ERROR):
    pass


@dataclass(frozen=True, slots=True)
class IllFormedLinkError(
    LinkErrorMixin, ClientError, message=YttgErrorMessage.ILL_FORMED_LINK
):
    """Not a valid link provided."""

    pass


@dataclass(frozen=True, slots=True)
class NoResultFoundError(
    LinkErrorMixin, ClientError, message=YttgErrorMessage.NO_RESULT_FOUND
):
    """A valid link that does not correspond to any video."""

    pass


@dataclass(frozen=True, slots=True)
class InvalidLanguageError(ClientError, message=YttgErrorMessage.INVALID_LANGUAGE):
    """Requested video has no audio in the provided language."""

    language: str
    """Chosen YouTube video language code."""
