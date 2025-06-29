from struct import pack as data_pack
from typing import Tuple
from uuid import UUID

class Minecraft:
    @staticmethod
    def varint(d: int) -> bytes:
        o = b''
        while True:
            b = d & 0x7F
            d >>= 7
            o += data_pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o

    @staticmethod
    def data(*payload: bytes) -> bytes:
        payload = b''.join(payload)
        return Minecraft.varint(len(payload)) + payload

    @staticmethod
    def short(integer: int) -> bytes:
        return data_pack('>H', integer)

    @staticmethod
    def long(integer: int) -> bytes:
        return data_pack('>q', integer)

    @staticmethod
    def handshake(target: Tuple[str, int], version: int, state: int) -> bytes:
        return Minecraft.data(Minecraft.varint(0x00),
                              Minecraft.varint(version),
                              Minecraft.data(target[0].encode()),
                              Minecraft.short(target[1]),
                              Minecraft.varint(state))

    @staticmethod
    def handshake_forwarded(target: Tuple[str, int], version: int, state: int, ip: str, uuid: UUID) -> bytes:
        return Minecraft.data(Minecraft.varint(0x00),
                              Minecraft.varint(version),
                              Minecraft.data(
                                  target[0].encode(),
                                  b"\x00",
                                  ip.encode(),
                                  b"\x00",
                                  uuid.hex.encode()
                              ),
                              Minecraft.short(target[1]),
                              Minecraft.varint(state))

    @staticmethod
    def login(protocol: int, username: str) -> bytes:
        if isinstance(username, str):
            username = username.encode()
        return Minecraft.data(Minecraft.varint(0x00 if protocol >= 391 else \
                                               0x01 if protocol >= 385 else \
                                               0x00),
                              Minecraft.data(username))

    @staticmethod
    def keepalive(protocol: int, num_id: int) -> bytes:
        return Minecraft.data(Minecraft.varint(0x0F if protocol >= 755 else \
                                               0x10 if protocol >= 712 else \
                                               0x0F if protocol >= 471 else \
                                               0x10 if protocol >= 464 else \
                                               0x0E if protocol >= 389 else \
                                               0x0C if protocol >= 386 else \
                                               0x0B if protocol >= 345 else \
                                               0x0A if protocol >= 343 else \
                                               0x0B if protocol >= 336 else \
                                               0x0C if protocol >= 318 else \
                                               0x0B if protocol >= 107 else \
                                               0x00),
                              Minecraft.long(num_id) if protocol >= 339 else \
                              Minecraft.varint(num_id))

    @staticmethod
    def chat(protocol: int, message: str) -> bytes:
        return Minecraft.data(Minecraft.varint(0x03 if protocol >= 755 else \
                                               0x03 if protocol >= 464 else \
                                               0x02 if protocol >= 389 else \
                                               0x01 if protocol >= 343 else \
                                               0x02 if protocol >= 336 else \
                                               0x03 if protocol >= 318 else \
                                               0x02 if protocol >= 107 else \
                                               0x01),
                              Minecraft.data(message.encode()))
