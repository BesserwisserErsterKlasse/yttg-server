from dataclasses import dataclass, field
from uuid import UUID, uuid4

from modules.tcp.types import Peer


@dataclass(slots=True)
class YttgSession:
    id: UUID = field(default_factory=uuid4, init=False)
    peer: Peer
    address: tuple[str, int]
