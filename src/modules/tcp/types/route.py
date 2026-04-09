from collections.abc import Awaitable, Callable
from typing import NamedTuple

from modules.tcp.types.request import RequestProtocol


class Route[Request: RequestProtocol](NamedTuple):
    constraint: Callable[[Request], bool]
    handler: Callable[[Request], Awaitable[None]]
