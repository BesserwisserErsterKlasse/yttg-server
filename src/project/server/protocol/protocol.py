from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest, new
from json import dumps, loads
from os import urandom
from struct import pack, unpack
from typing import Final, override

# isort: off
from env import env
from modules.tcp import TcpProtocol
from modules.tcp.types.peer import Peer
from project.server.protocol.converter import converter
from project.server.protocol.crypto import (
    aes256_ctr_decrypt,
    aes256_ctr_encrypt,
    ClientHello,
    compute_handshake_mac,
    derive_handshake_mac_key,
    KeyMaterial,
    ServerHello,
)
from project.server.types import (
    YttgCommand,
    YttgError,
    YttgRequest,
    YttgResponse,
    YttgSession,
)

match env.crypto.ml_kem:
    case 512:
        from pqcrypto.kem.ml_kem_512 import encrypt  # type: ignore[import-untyped]
    case 768:
        from pqcrypto.kem.ml_kem_768 import encrypt  # type: ignore[import-untyped]
    case 1024:
        from pqcrypto.kem.ml_kem_1024 import encrypt  # type: ignore[import-untyped]
# isort: on


PAYLOAD_SLICE: Final[slice] = slice(None, -32, None)
MAC_SLICE: Final[slice] = slice(-32, None, None)
SEQUENCE_NUMBER_SLICE: Final[slice] = slice(None, 8, None)
CIPHERTEXT_SLICE: Final[slice] = slice(8, None, None)


@dataclass(frozen=True, slots=True)
class YttgProtocol(TcpProtocol[YttgRequest, YttgResponse, YttgSession]):
    __header_size: int
    __pre_shared_key: bytes

    def __init__(self, header_size: int, psk: bytes) -> None:
        object.__setattr__(
            self, f'_{self.__class__.__name__}__header_size', header_size
        )
        object.__setattr__(self, f'_{self.__class__.__name__}__pre_shared_key', psk)

    @override
    async def create_session(self, peer: Peer, address: tuple[str, int]) -> YttgSession:
        receive_header: bytes = await peer.reader.readexactly(self.__header_size)
        raw_client_hello: bytes = await peer.reader.readexactly(int(receive_header))
        client_hello: ClientHello = converter.structure(
            obj=loads(raw_client_hello),
            cl=ClientHello,
        )
        if client_hello.magic != b'YTTG-PQ':
            raise ValueError('Invalid magic bytes')
        server_nonce: bytes = urandom(32)
        ciphertext, shared_secret = encrypt(client_hello.public_key)
        handshake_mac_key: bytes = derive_handshake_mac_key(
            shared_secret=shared_secret,
            pre_shared_key=self.__pre_shared_key,
            client_nonce=client_hello.nonce,
            server_nonce=server_nonce,
        )
        handshake_mac: bytes = compute_handshake_mac(
            handshake_mac_key=handshake_mac_key,
            raw_client_hello=raw_client_hello,
            server_nonce=server_nonce,
            ciphertext=ciphertext,
        )
        server_hello: ServerHello = ServerHello(
            nonce=server_nonce,
            ciphertext=ciphertext,
            handshake_mac=handshake_mac,
        )
        raw_server_hello: bytes = dumps(converter.unstructure(server_hello)).encode()
        send_header: bytes = f'{len(raw_server_hello):0>{self.__header_size}}'.encode()
        peer.writer.write(send_header + raw_server_hello)
        await peer.writer.drain()
        keys: KeyMaterial = KeyMaterial(
            shared_secret=shared_secret,
            pre_shared_key=self.__pre_shared_key,
            client_nonce=client_hello.nonce,
            server_nonce=server_hello.nonce,
            transcript_hash=sha256(raw_client_hello + raw_server_hello).digest(),
        )
        return YttgSession(peer=peer, address=address, keys=keys)

    @override
    async def receive(self, session: YttgSession) -> YttgRequest:
        header: bytes = await session.peer.reader.readexactly(self.__header_size)
        raw: bytes = await session.peer.reader.readexactly(int(header))
        payload, received_mac = raw[PAYLOAD_SLICE], raw[MAC_SLICE]
        expected_mac: bytes = new(session.keys.client_mac_key, payload, sha256).digest()
        if not compare_digest(expected_mac, received_mac):
            raise ValueError('Invalid MAC')
        sequence_number: int = unpack('>Q', payload[SEQUENCE_NUMBER_SLICE])[0]
        if sequence_number != session.receive_sequence_number:
            raise ValueError(f'Wrong sequence number: expected {(
                    session.receive_sequence_number
                )}, got {sequence_number}')
        plaintext: bytes = aes256_ctr_decrypt(
            key=session.keys.client_encryption_key,
            sequence_number=sequence_number,
            ciphertext=payload[CIPHERTEXT_SLICE],
        )
        session.receive_sequence_number += 1
        raw_command, raw_request = plaintext.split(sep=b'#', maxsplit=1)
        return converter.structure(
            obj=(loads(raw_request) | {'peer_id': session.id}),
            cl=YttgRequest.get_factory(YttgCommand(raw_command.decode())),
        )

    @override
    async def send(self, session: YttgSession, response: YttgResponse) -> None:
        unstructured_response: dict[str, object] = converter.unstructure(response)
        unstructured_response['response-kind'] = response.kind
        unstructured_response['status'] = response.status
        if isinstance(response, YttgError):
            unstructured_response['message'] = response.message
        raw_response: bytes = dumps(unstructured_response, sort_keys=True).encode()
        payload: bytes = pack('>Q', session.send_sequence_number) + aes256_ctr_encrypt(
            key=session.keys.server_encryption_key,
            sequence_number=session.send_sequence_number,
            plaintext=raw_response,
        )
        session.send_sequence_number += 1
        record_mac: bytes = new(session.keys.server_mac_key, payload, sha256).digest()
        record: bytes = payload + record_mac
        header: bytes = f'{len(record):0>{self.__header_size}}'.encode()
        session.peer.writer.write(header + record)
        await session.peer.writer.drain()
