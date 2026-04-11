from asyncio import sleep as asleep

from pyrogram.errors import InviteHashInvalid

from project.globalobjects import server
from project.pipelines.constraints import has_streams, photo, text, video
from project.pipelines.streams import OnLinkResponse
from project.pipelines.subscribe.const import FILLER_VIDEO_LINK
from project.pipelines.subscribe.namespace import OnClickResponse
from project.pipelines.utils import parse_channels
from project.server.types import InvalidChannelHashError, SubscribeRequest
from project.telegram import AcquiredChat, ExpectedMessage


async def get_channels(chat: AcquiredChat) -> list[str]:
    """Get a list of channels to subscribe to to get access to the bot."""

    await chat.send_text(FILLER_VIDEO_LINK)
    await chat.wait_for(ExpectedMessage(photo & has_streams, OnLinkResponse.STREAMS))
    await chat.click(OnLinkResponse.STREAMS, selector=(0, 0))
    response: OnClickResponse = await chat.wait_for(
        ExpectedMessage(text, name=OnClickResponse.CHANNELS_MESSAGE),
        ExpectedMessage(video, name=OnClickResponse.VIDEO_MESSAGE),
    )
    match response:
        case OnClickResponse.VIDEO_MESSAGE:
            return []
        case OnClickResponse.CHANNELS_MESSAGE:
            return parse_channels(chat[OnClickResponse.CHANNELS_MESSAGE])


async def subscribe(chat: AcquiredChat, request: SubscribeRequest) -> list[str]:
    """Subscribe to the specified Telegram channels."""

    subscribed: list[str] = []
    for channel in request.channels:
        try:
            await chat.subscribe(channel)
            subscribed.append(channel)
            await asleep(delay=1.0)
        except InviteHashInvalid:
            await server.send(
                peer_id=request.peer_id, response=InvalidChannelHashError(channel)
            )
    return subscribed
