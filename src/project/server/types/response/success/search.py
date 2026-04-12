from dataclasses import dataclass

from project.server.types.response.base import YttgResponse
from project.server.types.response.enums import ResponseStatus
from project.telegram.types import VideoResult


@dataclass(frozen=True, slots=True)
class SearchResponse(YttgResponse):
    offset: str | None
    """Opaque pagination token tied to the search query."""

    videos: list[VideoResult]
    """YouTube videos matching the query."""

    def __init__(self, offset: str | None, videos: list[VideoResult]) -> None:
        object.__setattr__(self, 'status', ResponseStatus.SUCCESS)
        object.__setattr__(self, 'offset', offset)
        object.__setattr__(self, 'videos', videos)
