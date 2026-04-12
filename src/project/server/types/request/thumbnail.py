from dataclasses import dataclass
from pathlib import Path

from project.server.types.request.base import (
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
)
from project.server.types.request.enums import YttgCommand


@dataclass(frozen=True, slots=True)
class ThumbnailRequest(
    ProviderRequestMixin,
    LinkRequestMixin,
    YttgRequest,
    command=YttgCommand.GET_THUMBNAIL,
):
    savepath: Path
    """Where to save the thumbnail."""
