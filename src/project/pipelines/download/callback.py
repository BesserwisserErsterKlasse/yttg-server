from asyncio import AbstractEventLoop
from collections.abc import Callable
from uuid import UUID

from project.globalobjects import server
from project.server.types import DownloadProgressResponse

type DownloadProgressCallback = Callable[[int, int], None]


def create_downloading_progress_callback(
    loop: AbstractEventLoop, peer_id: UUID
) -> DownloadProgressCallback:
    """Create a callback for downloading progress tracking."""

    def download_progress_callback(current: int, total: int) -> None:
        loop.create_task(server.send(peer_id, DownloadProgressResponse(current, total)))

    return download_progress_callback
