# flake8: noqa: E402
# isort: skip_file
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())  # Python3.14 behavior fix

from asyncio import run
from pathlib import Path

from project.globalobjects import server, tg
from project.pipelines import (
    download_video,
    get_channels,
    get_streams,
    get_thumbnail,
    select_stream,
    subscribe,
)
from project.server.types import (
    ChannelInfoRequest,
    ChannelInfoResponse,
    DownloadRequest,
    DownloadResponse,
    SearchRequest,
    SearchResponse,
    Stream,
    StreamInfoRequest,
    StreamInfoResponse,
    SubscribeRequest,
    SubscribeResponse,
    ThumbnailRequest,
    ThumbnailResponse,
    UnmatchedRequestError,
    YttgRequest,
)
from project.telegram.types import SearchResult


@server.on_request(StreamInfoRequest)
async def stream_info_request_handler(request: StreamInfoRequest) -> None:
    async with tg.acquire(request.provider) as chat:
        streams: dict[Stream, tuple[int, int]] | None = await get_streams(chat, request)
        if streams is None:
            return None
        await server.send(
            peer_id=request.peer_id,
            response=StreamInfoResponse(streams=list(streams.keys())),
        )


@server.on_request(DownloadRequest)
async def download_handler(request: DownloadRequest) -> None:
    async with tg.acquire(request.provider) as chat:
        streams: dict[Stream, tuple[int, int]] | None = await get_streams(chat, request)
        if streams is None:
            return None
        await select_stream(chat, streams[request.stream])
        savepath: Path | None = await download_video(chat, request)
        if savepath is None:
            return None
        await server.send(request.peer_id, DownloadResponse(savepath=savepath))


@server.on_request(ChannelInfoRequest)
async def channel_info_request_handler(request: ChannelInfoRequest) -> None:
    async with tg.acquire(request.provider) as chat:
        channels: list[str] = await get_channels(chat)
        await server.send(
            peer_id=request.peer_id,
            response=ChannelInfoResponse(channels),
        )


@server.on_request(SubscribeRequest)
async def subscribe_request_handler(request: SubscribeRequest) -> None:
    async with tg.acquire(request.provider) as chat:
        subscribed: list[str] = await subscribe(chat, request)
        await server.send(
            peer_id=request.peer_id,
            response=SubscribeResponse(subscribed),
        )


@server.on_request(SearchRequest)
async def search_request_handler(request: SearchRequest) -> None:
    result: SearchResult = await tg.search(request.query, request.offset)
    await server.send(
        peer_id=request.peer_id,
        response=SearchResponse(offset=result.offset, videos=result.videos),
    )


@server.on_request(ThumbnailRequest)
async def thumbnail_request_handler(request: ThumbnailRequest) -> None:
    async with tg.acquire(request.provider) as chat:
        await get_thumbnail(chat, request)
        await server.send(
            peer_id=request.peer_id,
            response=ThumbnailResponse(request.savepath),
        )


@server.on_unmatched_request
async def unmatched_request_handler(request: YttgRequest) -> None:
    await server.send(peer_id=request.peer_id, response=UnmatchedRequestError(request))


async def main() -> None:
    await tg.start()
    await server.start()


if __name__ == '__main__':
    run(main())
