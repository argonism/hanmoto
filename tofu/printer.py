from __future__ import annotations

import os
from enum import Enum
from types import TracebackType
from typing import Dict, Iterable, Optional, Type, TypeVar, Union

from escpos.printer import Network
from pydantic import BaseModel, Field

T = TypeVar("T", covariant=True)


class TofuException(Exception):
    ...


class TofuValueException(TofuException):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class Printable(object):
    ...


class TofuImage(Printable):
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.properties: Dict[str, Union[bool, int, str]] = {}
        super().__init__()

    def high_density_vertical(self) -> TofuImage:
        self.properties["high_density_vertical"] = True
        return self

    def high_density_horizontal(self) -> TofuImage:
        self.properties["high_density_horizontal"] = True
        return self

    def bitImageRaster(self) -> TofuImage:
        self.properties["impl"] = "bitImageRaster"
        return self

    def graphics(self) -> TofuImage:
        self.properties["impl"] = "graphics"
        return self

    def bitImageColumn(self) -> TofuImage:
        self.properties["impl"] = "bitImageColumn"
        return self

    def fragment_height(self, height: int = 960) -> TofuImage:
        self.properties["fragment_height"] = height
        return self

    def center(self) -> TofuImage:
        self.properties["center"] = True
        return self


class TofuText(Printable):
    def __init__(self, text: str) -> None:
        self.text = text
        self.properties: Dict[str, Union[bool, int, str]] = {}
        super().__init__()

    def center(self) -> TofuText:
        self.properties["align"] = "center"
        return self

    def right(self) -> TofuText:
        self.properties["align"] = "right"
        return self

    def left(self) -> TofuText:
        self.properties["align"] = "left"
        return self

    def font_a(self) -> TofuText:
        self.properties["font"] = 0
        return self

    def font_b(self) -> TofuText:
        self.properties["font"] = 1
        return self

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

    def width(self, width: int = 1) -> TofuText:
        if not (1 <= width <= 8):
            raise TofuValueException("width value must be 1 <= height =< 8")
        self.properties["width"] = width
        return self

    def height(self, height: int = 1) -> TofuText:
        if not (1 <= height <= 8):
            raise TofuValueException("height value must be 1 <= height =< 8")
        self.properties["height"] = height
        return self

    def density(self, density: int = 8) -> TofuText:
        if not (0 <= density <= 8):
            raise TofuValueException("height value must be 0 <= height =< 8")
        self.properties["density"] = density
        return self

    def invert(self, invert: bool = True) -> TofuText:
        self.properties["invert"] = invert
        return self

    def flip(self, flip: bool = True) -> TofuText:
        self.properties["flip"] = flip
        return self

    def double_width(self, double_width: bool = True) -> TofuText:
        self.properties["double_width"] = double_width
        return self

    def double_height(self, double_height: bool = True) -> TofuText:
        self.properties["double_height"] = double_height
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

    def _text(self, text: str, dw: bool = False, dh: bool = False) -> None:
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

    def print_sequence(self, sequence: Iterable[Printable]) -> None:
        for elem in sequence:
            if isinstance(elem, TofuText):
                set_params = elem.properties
                self.set(**set_params)
                self._text(elem.text + "\n")
            elif isinstance(elem, TofuImage):
                source_path = elem.image_path
                self.image(source_path, **elem.properties)

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
