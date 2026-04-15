from dataclasses import dataclass, field
from uuid import UUID, uuid4

from modules.tcp.types import Peer
from project.server.protocol.crypto import KeyMaterial


@dataclass(slots=True)
class YttgSession:
    id: UUID = field(default_factory=uuid4, init=False)
    peer: Peer
    address: tuple[str, int]
    keys: KeyMaterial
    send_sequence_number: int = field(default=0, init=False)
    receive_sequence_number: int = field(default=0, init=False)
