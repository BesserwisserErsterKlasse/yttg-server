from dataclasses import dataclass
from pathlib import Path

from project.server.types.request import Stream
from project.server.types.response.base import YttgResponse
from project.server.types.response.enums import ResponseStatus


@dataclass(frozen=True, slots=True)
class StreamInfoResponse(YttgResponse):
    streams: list[Stream]
    """YouTube video available streams."""

    def __init__(self, streams: list[Stream]) -> None:
        object.__setattr__(self, 'status', ResponseStatus.SUCCESS)
        object.__setattr__(self, 'streams', streams)


@dataclass(frozen=True, slots=True)
class DownloadResponse(YttgResponse):
    savepath: Path
    """Path where the file has been saved."""

    def __init__(self, savepath: Path) -> None:
        object.__setattr__(self, 'status', ResponseStatus.SUCCESS)
        object.__setattr__(self, 'savepath', savepath)
