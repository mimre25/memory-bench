from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any, Callable
import psutil
from pydantic import BaseModel
import pydantic
import orjson
import sys
import gc
import signal

from data import data
from util import wait_for_signal


class PydanticModel(BaseModel):
    name: str
    age: int
    children: list["PydanticModel"] = []

@dataclass
class Dataclass():
    name: str
    age: int
    children: list["Dataclass"]


    @classmethod
    def parse(cls, data: bytes | dict) -> "Dataclass":
        if isinstance(data, bytes):
            dct = json.loads(data)
        else:
            dct = data
        children = [Dataclass.parse(c) for c in dct["children"]]
        return cls(name=dct["name"], age=dct["age"], children = children)



def parse(data: bytes, fun: Callable[[bytes], Any]) -> Any:
    return fun(data)


if __name__ == "__main__":
    flavor = sys.argv[1]

    fun = lambda *args: None
    if flavor == "json":
        fun = json.loads
    if flavor == "orjson":
        fun = orjson.loads
    if flavor == "dataclass":
        fun = Dataclass.parse
    if flavor == "pydantic":
        if pydantic.__version__[0] == "2":
            pydantic_fun = PydanticModel.model_validate_json
        else:
            pydantic_fun = PydanticModel.parse_raw
        fun = pydantic_fun
    proc = psutil.Process()
    result = fun(data)
    proc.parent().send_signal(signal.SIGUSR1)
    wait_for_signal(signal.SIGUSR2)
    mem = proc.memory_info().rss
    print(f"{flavor} Usage before garbage collection: {round(mem/1024/1024, 2)} MB")
    gc.collect()
    mem = proc.memory_info().rss
    print(f"{flavor} Usage after garbage collection: {round(mem/1024/1024, 2)} MB")

