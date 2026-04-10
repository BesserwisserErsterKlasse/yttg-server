from pathlib import Path

from project.globalobjects import server
from project.pipelines.constraints import audio, text, video
from project.pipelines.download.namespace import OnStreamSelectionResponse
from project.pipelines.utils import parse_video_title
from project.server.types import DownloadRequest, NotSubscribedError, Stream
from project.telegram import AcquiredChat, ExpectedMessage


async def download_video(chat: AcquiredChat, request: DownloadRequest) -> Path | None:
    """Download the requested YouTube video."""

    response: OnStreamSelectionResponse = await chat.wait_for(
        ExpectedMessage(
            audio if request.stream == Stream.AUDIO else video,
            name=OnStreamSelectionResponse.MEDIA_MESSAGE,
        ),
        ExpectedMessage(text, name=OnStreamSelectionResponse.NOT_SUBSCRIBED_ERROR),
    )
    match response:
        case OnStreamSelectionResponse.NOT_SUBSCRIBED_ERROR:
            await server.send(
                peer_id=request.peer_id,
                response=NotSubscribedError(provider=request.provider),
            )
            return None
        case OnStreamSelectionResponse.MEDIA_MESSAGE:
            video_title: str = parse_video_title(
                chat[OnStreamSelectionResponse.MEDIA_MESSAGE]
            )
            savepath: Path = request.get_savepath(title=video_title)
            await chat[OnStreamSelectionResponse.MEDIA_MESSAGE].download(
                file_name=str(savepath)
            )
            return savepath
