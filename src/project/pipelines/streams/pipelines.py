from project.globalobjects import server
from project.pipelines.constraints import (
    has_streams,
    ill_formed_link_error,
    no_result_found_error,
    photo,
)
from project.pipelines.streams.namespace import OnLinkResponse
from project.pipelines.utils import parse_streams
from project.server.types import (
    DownloadRequest,
    IllFormedLinkError,
    NoResultFoundError,
    Stream,
    StreamInfoRequest,
)
from project.telegram import AcquiredChat, ExpectedMessage

type LinkRequest = DownloadRequest | StreamInfoRequest


async def get_streams(
    chat: AcquiredChat, request: LinkRequest
) -> dict[Stream, tuple[int, int]] | None:
    """Get YouTube video streams."""

    await chat.send_text(request.link)
    response: OnLinkResponse = await chat.wait_for(
        ExpectedMessage(photo & has_streams, OnLinkResponse.STREAMS),
        ExpectedMessage(ill_formed_link_error, OnLinkResponse.ILL_FORMED_LINK_ERROR),
        ExpectedMessage(no_result_found_error, OnLinkResponse.NO_RESULTS_FOUND_ERROR),
    )
    match response:
        case OnLinkResponse.ILL_FORMED_LINK_ERROR:
            await server.send(
                peer_id=request.peer_id,
                response=IllFormedLinkError(link=request.link),
            )
            return None
        case OnLinkResponse.NO_RESULTS_FOUND_ERROR:
            await server.send(
                peer_id=request.peer_id,
                response=NoResultFoundError(link=request.link),
            )
            return None
        case OnLinkResponse.STREAMS:
            return parse_streams(chat[OnLinkResponse.STREAMS])


async def select_stream(chat: AcquiredChat, stream_selector: tuple[int, int]) -> None:
    """Select a YouTube video stream."""

    await chat.click(OnLinkResponse.STREAMS, stream_selector)
