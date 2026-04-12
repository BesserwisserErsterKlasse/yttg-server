from abc import ABC
from dataclasses import dataclass
from typing import Any, ClassVar

from project.server.types.response.enums import ResponseStatus, YttgErrorMessage
from project.server.utils.case import to_dash_case


@dataclass(frozen=True)
class YttgResponse(ABC):
    kind: ClassVar[str]
    """Response kind."""

    status: ClassVar[ResponseStatus]
    """Response status."""

    def __init_subclass__(cls, status: ResponseStatus | None = None) -> None:
        cls.kind = to_dash_case(cls.__name__)
        if status is not None:
            cls.status = status


@dataclass(frozen=True, slots=True)
class YttgSuccess(YttgResponse, status=ResponseStatus.SUCCESS):
    pass


@dataclass(frozen=True, slots=True)
class YttgError(YttgResponse, ABC):
    message: ClassVar[YttgErrorMessage]
    """Response error message."""

    def __init_subclass__(
        cls, message: YttgErrorMessage | None = None, **kwargs: Any
    ) -> None:
        super().__init_subclass__(**kwargs)
        if message is not None:
            cls.message = message
