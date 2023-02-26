from __future__ import annotations

import os
from enum import Enum
from types import TracebackType
from typing import Iterable, Optional, Type, Union

from escpos.printer import Dummy, Escpos, Network
from pydantic import BaseModel

from .exceptions import HmtValueException
from .printables import HmtImage, HmtText, Printable


class HmtPrinterType(Enum):
    network = "network"
    dummy = "dummy"

    @classmethod
    def get_types(cls) -> list:
        return [i.name for i in cls]


class HmtNetworkConf(BaseModel):
    host: str = ""
    port: int = 9100
    timeout: int = 60


class HmtPrinterConf(BaseModel):
    printer_type: HmtPrinterType = HmtPrinterType.network
    conf: HmtNetworkConf = HmtNetworkConf()

class HmtConf(BaseModel)

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
    def from_conf(cls, conf: HmtConf) -> Hanmoto:
        printer_type = conf.printer_type
        if printer_type == "network":
            return cls.from_network(**conf.conf.dict())
        elif printer_type == "dummy":
            return cls.from_dummy()
        else:
            raise HmtValueException(f"Unknown printer type: {printer_type}")

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
                image_src = elem.image_src
                self.printer.image(image_src, **elem.properties)

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
        self.printer.close()
