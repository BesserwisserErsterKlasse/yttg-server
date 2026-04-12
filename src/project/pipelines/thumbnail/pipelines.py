from project.globalobjects import server
from project.pipelines.constraints import (
    has_streams,
    ill_formed_link_error,
    no_result_found_error,
    photo,
)
from project.pipelines.thumbnail.namespace import OnLinkResponse
from project.server.types import (
    IllFormedLinkError,
    NoResultFoundError,
    ThumbnailRequest,
)
from project.telegram import AcquiredChat, ExpectedMessage


async def get_thumbnail(chat: AcquiredChat, request: ThumbnailRequest) -> None:
    """Get YouTube video thumbnail."""

    await chat.send_text(request.link)
    response: OnLinkResponse = await chat.wait_for(
        ExpectedMessage(photo & has_streams, OnLinkResponse.THUMBNAIL),
        ExpectedMessage(ill_formed_link_error, OnLinkResponse.ILL_FORMED_LINK_ERROR),
        ExpectedMessage(no_result_found_error, OnLinkResponse.NO_RESULTS_FOUND_ERROR),
    )
    match response:
        case OnLinkResponse.ILL_FORMED_LINK_ERROR:
            await server.send(
                peer_id=request.peer_id,
                response=IllFormedLinkError(link=request.link),
            )
        case OnLinkResponse.NO_RESULTS_FOUND_ERROR:
            await server.send(
                peer_id=request.peer_id,
                response=NoResultFoundError(link=request.link),
            )
        case OnLinkResponse.THUMBNAIL:
            await chat[OnLinkResponse.THUMBNAIL].download(str(request.savepath))
