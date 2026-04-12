from dataclasses import dataclass
from pathlib import Path

from project.server.types.response.base import YttgSuccess


@dataclass(frozen=True, slots=True)
class ThumbnailResponse(YttgSuccess):
    savepath: Path
    """Path to the saved thumbnail."""
