from asyncio import (
    AbstractServer,
    Semaphore,
    start_server,
    StreamReader,
    StreamWriter,
)
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, NoReturn
from uuid import UUID

from modules.tcp.types import Peer, RequestProtocol, Route, SessionProtocol, TcpProtocol


@dataclass(slots=True)
class TcpServer[Request: RequestProtocol, Response, Session: SessionProtocol]:
    __protocol: TcpProtocol[Request, Response, Session]
    __host: str
    __port: int
    __semaphore: Semaphore
    __sessions: dict[UUID, Session]
    __routes: list[Route[Request]]

    async def start(self) -> NoReturn:  # type: ignore[misc]
        """Start the server."""

        server: AbstractServer = await start_server(
            self.__accept,
            host=self.__host,
            port=self.__port,
            reuse_address=True,
        )
        async with server:
            await server.serve_forever()

    async def send(self, peer_id: UUID, response: Response) -> None:
        """Send response back to the request sender."""

        await self.__protocol.send(self.__sessions[peer_id], response)

    def add_route(self, route: Route[Any]) -> None:
        """Add a new route."""

        self.__routes.append(route)

    def __init__(
        self,
        protocol: TcpProtocol[Request, Response, Session],
        max_connections: int,
        host: str,
        port: int,
    ) -> None:
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        self.__semaphore = Semaphore(max_connections)
        self.__sessions = {}
        self.__routes = []

    async def __receive(self, session: Session) -> None:
        with suppress(Exception):
            while True:
                request: Request = await self.__protocol.receive(session)
                for constraint, handler in self.__routes:
                    if constraint(request):
                        await handler(request)
                        break

    async def __accept(self, reader: StreamReader, writer: StreamWriter) -> None:
        async with self.__semaphore:
            session: Session = await self.__protocol.create_session(
                peer=Peer(reader, writer), address=writer.get_extra_info('peername')
            )
            self.__sessions[session.id] = session
            try:
                await self.__receive(session)
            finally:
                self.__sessions.pop(session.id, None)
                writer.close()
                with suppress(ConnectionError):
                    await writer.wait_closed()
