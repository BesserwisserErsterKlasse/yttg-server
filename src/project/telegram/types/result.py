from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoResult:
    link: str
    """Link to a YouTube video."""

    thumbnail_link: str
    """Link to a YouTube video thumbnail."""

    title: str
    """YouTube video title."""

    duration: int
    """YouTube video duration in seconds."""

    views: str | None
    """Approximate number of views, e.g. `'47M'`"""


@dataclass(frozen=True, slots=True)
class SearchResult:
    offset: str | None
    """Opaque pagination token tied to the search query."""

    videos: list[VideoResult]
    """YouTube videos matching the query."""
