from typing import Protocol
from uuid import UUID

from modules.tcp.types.peer import Peer


class SessionProtocol(Protocol):
    id: UUID
    peer: Peer
