from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from modules.tcp import TcpServer
from modules.tcp.types import Route
from project.server.protocol import YttgProtocol
from project.server.types import YttgRequest, YttgResponse, YttgSession

type Handler[RequestT: YttgRequest] = Callable[[RequestT], Awaitable[None]]
type HandlerDecorator[RequestT: YttgRequest] = Callable[
    [Handler[RequestT]], Handler[RequestT]
]


def match_request[RequestT: YttgRequest](
    request_type: type[RequestT],
) -> Callable[[RequestT], bool]:
    return lambda request: request.command == request_type.command


@dataclass(slots=True)
class YttgServer(TcpServer[YttgRequest, YttgResponse, YttgSession]):
    def __init__(
        self,
        protocol: YttgProtocol,
        max_connections: int,
        host: str,
        port: int,
    ) -> None:
        super(YttgServer, self).__init__(protocol, max_connections, host, port)

    def on_request[RequestT: YttgRequest](
        self, request_type: type[RequestT]
    ) -> HandlerDecorator[RequestT]:
        """Register handler for a specific request type."""

        def decorator(handler: Handler[RequestT]) -> Handler[RequestT]:
            self.add_route(Route(match_request(request_type), handler))
            return handler

        return decorator

    def on_unmatched_request(
        self, handler: Handler[YttgRequest]
    ) -> Handler[YttgRequest]:
        """Register handler for unmatched requests."""

        self.add_route(Route(constraint=(lambda _: True), handler=handler))
        return handler
