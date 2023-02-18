from __future__ import annotations

import abc
import os
from types import TracebackType
from typing import Dict, Iterable, Optional, Type, TypeVar, Union

from escpos.printer import Dummy, Escpos, Network

T = TypeVar("T", covariant=True)


class HmtException(Exception):
    """
    Hanmoto Base Exception.
    """

    ...


class HmtValueException(HmtException):
    """
    Hanmoto Value Exception.
    """

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class Printable(metaclass=abc.ABCMeta):
    """
    Abstract base class for printable objects that can be passed to Hanmoto.
    """

    ...


PROPERTIES_TYPE = Dict[str, Union[bool, int, str]]


class HmtImage(Printable):
    f"""
    Printable class for printing a image.

    ...

    Attributes
    ----------
    image_path : str
        source image path

    Parameters
    ----------
    image_path : str
        Image source path
    properties : {PROPERTIES_TYPE}, optional
        Dict that specify image style.
        see https://github.com/python-escpos/python-escpos/blob/master/src/escpos/escpos.py#L123 for details.
    """

    def __init__(
        self, image_path: str, properties: PROPERTIES_TYPE = {}
    ) -> None:
        self.image_path = image_path
        self.__properties: PROPERTIES_TYPE = properties
        super().__init__()

    @property
    def properties(self) -> PROPERTIES_TYPE:
        return self.__properties

    def high_density_vertical(self) -> HmtImage:
        self.__properties["high_density_vertical"] = True
        return self

    def high_density_horizontal(self) -> HmtImage:
        self.__properties["high_density_horizontal"] = True
        return self

    def bitImageRaster(self) -> HmtImage:
        self.__properties["impl"] = "bitImageRaster"
        return self

    def graphics(self) -> HmtImage:
        self.__properties["impl"] = "graphics"
        return self

    def bitImageColumn(self) -> HmtImage:
        self.__properties["impl"] = "bitImageColumn"
        return self

    def fragment_height(self, height: int = 960) -> HmtImage:
        self.__properties["fragment_height"] = height
        return self

    def center(self) -> HmtImage:
        self.__properties["center"] = True
        return self


class HmtText(Printable):
    f"""
    Printable class for printing a text.
    ...

    Attributes
    ----------
    text : str
        text to print

    Parameters
    ----------
    text : str
        Image source path
    properties : {PROPERTIES_TYPE}, optional
        Dict that specify text style.
        see https://github.com/python-escpos/python-escpos/blob/master/src/escpos/escpos.py#L624 for details.
    """

    def __init__(self, text: str, properties: PROPERTIES_TYPE = {}) -> None:
        self.text = text
        self.__properties: PROPERTIES_TYPE = properties
        super().__init__()

    @property
    def properties(self) -> PROPERTIES_TYPE:
        return self.__properties

    def center(self) -> HmtText:
        self.__properties["align"] = "center"
        return self

    def right(self) -> HmtText:
        self.__properties["align"] = "right"
        return self

    def left(self) -> HmtText:
        self.__properties["align"] = "left"
        return self

    def font_a(self) -> HmtText:
        self.__properties["font"] = 0
        return self

    def font_b(self) -> HmtText:
        self.__properties["font"] = 1
        return self

    def bold(self, bold: bool = True) -> HmtText:
        self.__properties["bold"] = bold
        return self

    def underline(self, underline: int = 1) -> HmtText:
        if not (0 <= underline <= 2):
            raise HmtValueException(
                "underline value must be 0 <= underline =< 2"
            )
        self.__properties["underline"] = underline
        return self

    def width(self, width: int = 1) -> HmtText:
        if not (1 <= width <= 8):
            raise HmtValueException("width value must be 1 <= height =< 8")
        self.__properties["width"] = width
        return self

    def height(self, height: int = 1) -> HmtText:
        if not (1 <= height <= 8):
            raise HmtValueException("height value must be 1 <= height =< 8")
        self.__properties["height"] = height
        return self

    def density(self, density: int = 8) -> HmtText:
        if not (0 <= density <= 8):
            raise HmtValueException("height value must be 0 <= height =< 8")
        self.__properties["density"] = density
        return self

    def invert(self, invert: bool = True) -> HmtText:
        self.__properties["invert"] = invert
        return self

    def flip(self, flip: bool = True) -> HmtText:
        self.__properties["flip"] = flip
        return self

    def double_width(self, double_width: bool = True) -> HmtText:
        self.__properties["double_width"] = double_width
        return self

    def double_height(self, double_height: bool = True) -> HmtText:
        self.__properties["double_height"] = double_height
        return self


class Hanmoto(object):
    """
    Printer class for printing printable objects.
    ...

    Attributes
    ----------
    printer : Escpos
        printer class from escpos package

    Parameters
    ----------
    printer : Escpos
        printer class from escpos package
    """

    def __init__(self, printer: Escpos) -> None:
        self.printer = printer
        self.printer.charcode("CP932")
        self.printer._raw(b"\x1c\x43\x01")

    @classmethod
    def from_network(
        cls, host: str = "", port: int = 9100, timeout: int = 60
    ) -> Hanmoto:
        """
        Initialize Hanmoto with network connected printer

        Parameters
        ----------
        host : str
            hostname, ip address of the printer
        port : int, optional
            port number of the printer
        timeout : int, optional
            timeout in seconds for the escpos-library

        Returns
        -------
        hanmoto : Hanmoto
            instance of Hanmoto that is initialized with Network printer

        See Also
        --------
        https://github.com/python-escpos/python-escpos/blob/master/src/escpos/printer.py#L209
        """
        if (
            "HANMOTO_PRINTER_IP" in os.environ
            and os.environ["HANMOTO_PRINTER_IP"]
        ):
            host = os.environ["HANMOTO_PRINTER_IP"]
        if not host:
            raise HmtValueException("host param is needed to be specified")

        printer = Network(host, port=port, timeout=timeout)
        instance = cls(printer)
        return instance

    @classmethod
    def from_dummy(cls) -> Hanmoto:
        """
        Initialize Hanmoto with dummy printer

        Returns
        -------
        hanmoto : Hanmoto
            instance of Hanmoto that is initialized with Dummy printer

        See Also
        --------
        https://github.com/python-escpos/python-escpos/blob/master/src/escpos/printer.py#L330
        """
        printer = Dummy()
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
            if isinstance(elem, HmtText):
                set_params = elem.properties
                self.printer.set(**set_params)
                self._text(elem.text + "\n")
            elif isinstance(elem, HmtImage):
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
