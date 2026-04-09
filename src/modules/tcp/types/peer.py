from asyncio import StreamReader, StreamWriter
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Peer:
    reader: StreamReader
    writer: StreamWriter
