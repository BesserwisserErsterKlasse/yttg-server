from asyncio import sleep as asleep
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Final

from pyrogram.errors import FloodWait

type AsyncFunction[**Args, Ret] = Callable[Args, Awaitable[Ret]]
type AsyncFunctionDecorator[**Args, Ret] = Callable[
    [AsyncFunction[Args, Ret]], AsyncFunction[Args, Ret]
]


RETRY_TIMES: Final[int] = 3


def retry[**Args, Ret](func: AsyncFunction[Args, Ret]) -> AsyncFunction[Args, Ret]:
    """Retry on FloodWait a specified number of times."""

    @wraps(func)
    async def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret:
        for _ in range(RETRY_TIMES):
            try:
                return await func(*args, **kwargs)
            except FloodWait as flood_wait:
                assert isinstance(flood_wait.value, int)
                await asleep(delay=flood_wait.value)
        raise RuntimeError(f'{func.__name__} failed {RETRY_TIMES} times')

    return wrapper
