from dataclasses import dataclass
from functools import cache
from os import getenv
import struct
from typing import Protocol


def config_dict():
    return dict(
        host=getenv("HOST", "0.0.0.0"),
        port=int(getenv("PORT", "8100")),
        keepalive_timeout=int(getenv("KEEPALIVE_TIMEOUT", "4")),
    )


def clinet_config():
    conf = config_dict()
    client_host = getenv("CLIENT_HOST", "localhost")
    return dict(
        url=f"ws://{client_host}:{conf['port']}",
        transports=["websocket", "polling"],
        wait_timeout=2,
    )


# TASK_PERIOD = 1 / 25
TASK_PERIOD = 2

EVENT_XY = "xy"


class IStruct(Protocol):

    @classmethod
    def __schema(cls) -> str:
        pass

    def model_dump(self) -> bytes:
        pass

    @classmethod
    def model_validate(cls, data: bytes):
        pass


@dataclass
class StructXY:
    x1: int
    y1: int
    x2: int
    y2: int

    @classmethod
    @cache
    def __schema(cls) -> str:
        return ">qqqq"

    def model_dump(self) -> bytes:
        return struct.pack(self.__schema(), self.x1, self.y1, self.x2, self.y2)

    @classmethod
    def model_validate(cls, data: bytes):
        values = struct.unpack(cls.__schema(), data)
        return cls(*values)
