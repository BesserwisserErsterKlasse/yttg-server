from dataclasses import dataclass

from project.server.types.response.base import YttgSuccess


@dataclass(frozen=True, slots=True)
class DownloadProgressResponse(YttgSuccess):
    current: int
    """Number of bytes downloaded so far."""

    total: int
    """File size in bytes."""
