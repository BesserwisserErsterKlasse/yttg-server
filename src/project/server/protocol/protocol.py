from dataclasses import dataclass
from json import dumps, loads
from typing import Any, override

from modules.tcp import TcpProtocol
from modules.tcp.types.peer import Peer
from project.server.protocol.converter import converter
from project.server.types import (
    YttgCommand,
    YttgError,
    YttgRequest,
    YttgResponse,
    YttgSession,
)


@dataclass(frozen=True, slots=True)
class YttgProtocol(TcpProtocol[YttgRequest, YttgResponse, YttgSession]):
    header_size: int

    @override
    async def create_session(self, peer: Peer, address: tuple[str, int]) -> Any:
        return YttgSession(peer=peer, address=address)

    @override
    async def receive(self, session: YttgSession) -> YttgRequest:
        header: bytes = await session.peer.reader.readexactly(self.header_size)
        body: bytes = await session.peer.reader.readexactly(int(header))
        raw_command, raw_request = body.split(sep=b'#', maxsplit=1)
        return converter.structure(
            obj=(loads(raw_request) | {'peer_id': session.id}),
            cl=YttgRequest.get_factory(YttgCommand(raw_command.decode())),
        )

    @override
    async def send(self, session: YttgSession, response: YttgResponse) -> None:
        serialized_response: dict[str, object] = converter.unstructure(response)
        serialized_response['response-kind'] = response.kind
        serialized_response['status'] = response.status
        if isinstance(response, YttgError):
            serialized_response['message'] = response.message
        raw_response: bytes = dumps(serialized_response, sort_keys=True).encode()
        header: bytes = f'{len(raw_response):0>16}'.encode()
        session.peer.writer.write(header + raw_response)
        await session.peer.writer.drain()
