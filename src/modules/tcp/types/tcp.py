from abc import ABC, abstractmethod

from modules.tcp.types.peer import Peer
from modules.tcp.types.session import SessionProtocol


class TcpProtocol[Request, Response, Session: SessionProtocol](ABC):
    @abstractmethod
    async def create_session(self, peer: Peer, address: tuple[str, int]) -> Session:
        """Create a session for a new client."""

        raise NotImplementedError

    @abstractmethod
    async def receive(self, session: Session) -> Request:
        """Receive a new request from the client."""

        raise NotImplementedError

    @abstractmethod
    async def send(self, session: Session, response: Response) -> None:
        """Send a response back to the client."""

        raise NotImplementedError
