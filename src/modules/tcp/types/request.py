from typing import Protocol
from uuid import UUID


class RequestProtocol(Protocol):
    @property
    def peer_id(self) -> UUID:
        raise NotImplementedError
