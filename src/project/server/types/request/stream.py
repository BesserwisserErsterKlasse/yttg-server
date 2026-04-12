from dataclasses import dataclass
from pathlib import Path

from project.server.types.request.base import (
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
)
from project.server.types.request.enums import Stream, YttgCommand


@dataclass(frozen=True, slots=True)
class StreamInfoRequest(
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.GET_STREAMS,
):
    pass


@dataclass(frozen=True, slots=True)
class DownloadRequest(
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.DOWNLOAD,
):
    stream: Stream
    """YouTube stream to download."""

    language: str
    """Preffered language of the audio."""

    folder: Path
    """Folder where to save the file."""

    name: str = '{title}'
    """Local name of the media file."""

    def get_savepath(self, title: str) -> Path:
        """Construct a path where to download the video."""

        return self.folder / (f'{self.name.format(title=title)}.{(
                'mp3' if self.stream == Stream.AUDIO else 'mp4'
            )}')
