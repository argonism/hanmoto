from __future__ import annotations

import os
from types import TracebackType
from typing import Dict, Iterable, Optional, Type, TypeVar, Union

from escpos.printer import Escpos, Network

T = TypeVar("T", covariant=True)


class TofuException(Exception):
    ...


class TofuValueException(TofuException):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class Printable(object):
    ...


PROPERTIES_TYPE = Dict[str, Union[bool, int, str]]


class TofuImage(Printable):
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.__properties: PROPERTIES_TYPE = {}
        super().__init__()

    @property
    def properties(self) -> PROPERTIES_TYPE:
        return self.__properties

    def high_density_vertical(self) -> TofuImage:
        self.__properties["high_density_vertical"] = True
        return self

    def high_density_horizontal(self) -> TofuImage:
        self.__properties["high_density_horizontal"] = True
        return self

    def bitImageRaster(self) -> TofuImage:
        self.__properties["impl"] = "bitImageRaster"
        return self

    def graphics(self) -> TofuImage:
        self.__properties["impl"] = "graphics"
        return self

    def bitImageColumn(self) -> TofuImage:
        self.__properties["impl"] = "bitImageColumn"
        return self

    def fragment_height(self, height: int = 960) -> TofuImage:
        self.__properties["fragment_height"] = height
        return self

    def center(self) -> TofuImage:
        self.__properties["center"] = True
        return self


class TofuText(Printable):
    def __init__(self, text: str) -> None:
        self.text = text
        self.__properties: PROPERTIES_TYPE = {}
        super().__init__()

    @property
    def properties(self) -> PROPERTIES_TYPE:
        return self.__properties

    def center(self) -> TofuText:
        self.__properties["align"] = "center"
        return self

    def right(self) -> TofuText:
        self.__properties["align"] = "right"
        return self

    def left(self) -> TofuText:
        self.__properties["align"] = "left"
        return self

    def font_a(self) -> TofuText:
        self.__properties["font"] = 0
        return self

    def font_b(self) -> TofuText:
        self.__properties["font"] = 1
        return self

    def bold(self, bold: bool = True) -> TofuText:
        self.__properties["bold"] = bold
        return self

    def underline(self, underline: int = 1) -> TofuText:
        if not (0 <= underline <= 2):
            raise TofuValueException(
                "underline value must be 0 <= underline =< 2"
            )
        self.__properties["underline"] = underline
        return self

    def width(self, width: int = 1) -> TofuText:
        if not (1 <= width <= 8):
            raise TofuValueException("width value must be 1 <= height =< 8")
        self.__properties["width"] = width
        return self

    def height(self, height: int = 1) -> TofuText:
        if not (1 <= height <= 8):
            raise TofuValueException("height value must be 1 <= height =< 8")
        self.__properties["height"] = height
        return self

    def density(self, density: int = 8) -> TofuText:
        if not (0 <= density <= 8):
            raise TofuValueException("height value must be 0 <= height =< 8")
        self.__properties["density"] = density
        return self

    def invert(self, invert: bool = True) -> TofuText:
        self.__properties["invert"] = invert
        return self

    def flip(self, flip: bool = True) -> TofuText:
        self.__properties["flip"] = flip
        return self

    def double_width(self, double_width: bool = True) -> TofuText:
        self.__properties["double_width"] = double_width
        return self

    def double_height(self, double_height: bool = True) -> TofuText:
        self.__properties["double_height"] = double_height
        return self


class Tofu(object):
    def __init__(self, printer: Escpos) -> None:
        self.printer = printer
        self.printer.charcode("CP932")
        self.printer._raw(b"\x1c\x43\x01")

    @classmethod
    def from_network(
        cls, host: str = "", port: int = 9100, timeout: int = 60
    ) -> Tofu:
        if "TOFU_PRINTER_IP" in os.environ and os.environ["TOFU_PRINTER_IP"]:
            host = os.environ["TOFU_PRINTER_IP"]
        if not host:
            raise TofuValueException("host param is needed to be specified")

        printer = Network(host, port=port, timeout=timeout)
        instance = cls(printer)
        return instance

    def _text(self, text: str, dw: bool = False, dh: bool = False) -> None:
        self.printer._raw(b"\x1c\x26")
        n = 0x00
        if dw:
            n += 0x04
        if dh:
            n += 0x08
        if n != 0x00:
            self.printer._raw(b"\x1c\x21" + n.to_bytes(1, byteorder="big"))
        self.printer._raw(text.encode("shift_jis", "ignore"))
        if n != 0x00:
            self.printer._raw(b"\x1c\x21\x00")
        self.printer._raw(b"\x1c\x2e")

    def print_sequence(self, sequence: Iterable[Printable]) -> None:
        for elem in sequence:
            if isinstance(elem, TofuText):
                set_params = elem.properties
                self.printer.set(**set_params)
                self._text(elem.text + "\n")
            elif isinstance(elem, TofuImage):
                source_path = elem.image_path
                self.printer.image(source_path, **elem.properties)

    def __enter__(self) -> None:
        self.printer.open()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.printer.cut()
        self.printer.close()
