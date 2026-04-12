from dataclasses import dataclass
from pathlib import Path

from project.server.types.request import Stream
from project.server.types.response.base import YttgSuccess


@dataclass(frozen=True, slots=True)
class StreamInfoResponse(YttgSuccess):
    streams: list[Stream]
    """YouTube video available streams."""


@dataclass(frozen=True, slots=True)
class DownloadResponse(YttgSuccess):
    savepath: Path
    """Path where the file has been saved."""
