from dataclasses import dataclass

from project.server.types.response.base import YttgSuccess
from project.telegram.types import VideoResult


@dataclass(frozen=True, slots=True)
class SearchResponse(YttgSuccess):
    offset: str | None
    """Opaque pagination token tied to the search query."""

    videos: list[VideoResult]
    """YouTube videos matching the query."""
