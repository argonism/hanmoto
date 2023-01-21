from __future__ import annotations
from types import TracebackType
from typing import Union, Dict, List, Optional, TypeVar, Type
import os

from escpos.printer import Network

T = TypeVar("T", covariant=True)


class TofuException(Exception):
    ...


class TofuValueException(TofuException):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class Printable(object):
    ...


class TofuText(Printable):
    def __init__(self, text: str) -> None:
        self.text = text
        self.properties: Dict[str, Union[bool, int]] = {}

    def bold(self, bold: bool = True) -> TofuText:
        self.properties["bold"] = bold
        return self

    def underline(self, underline: int = 1) -> TofuText:
        if not (0 <= underline <= 2):
            raise TofuValueException(
                "underline value must be 0 <= underline =< 2"
            )
        self.properties["underline"] = underline
        return self

    def invert(self, invert: bool = True) -> TofuText:
        self.properties["invert"] = invert
        return self

    def flip(self, flip: bool = True) -> TofuText:
        self.properties["flip"] = flip
        return self


class Tofu(Network):
    _instance: Union[None, Tofu] = None

    def __init__(self, ip_addr: str) -> None:
        raise NotImplementedError(
            f"{self.__class__.__name__} cannot be instanciated directly"
        )

    @classmethod
    def get_instance(cls) -> Tofu:
        if cls._instance is not None:
            return cls._instance

        cls.ip_addr = os.environ["TOFU_PRINTER_IP"]
        instance = cls.__new__(cls)
        super().__init__(instance, cls.ip_addr)
        instance._setup()
        cls._instance = instance
        return cls._instance

    def _setup(self) -> None:
        self.charcode("CP932")
        self._raw(b"\x1c\x43\x01")

    def text(self, text: str, dw: bool = False, dh: bool = False) -> None:
        self._raw(b"\x1c\x26")
        n = 0x00
        if dw:
            n += 0x04
        if dh:
            n += 0x08
        if n != 0x00:
            self._raw(b"\x1c\x21" + n.to_bytes(1, byteorder="big"))
        self._raw(text.encode("shift_jis", "ignore"))
        if n != 0x00:
            self._raw(b"\x1c\x21\x00")
        self._raw(b"\x1c\x2e")

    def __enter__(self) -> None:
        self.open()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.cut()
        self.close()
