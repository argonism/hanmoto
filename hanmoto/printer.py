from __future__ import annotations

import os
from types import TracebackType
from typing import Iterable, List, Optional, Type

from escpos.printer import Dummy, Escpos, Network

from .config import HmtConf, HmtPrinterType
from .exceptions import HmtValueException
from .localizer import HmtLocalizerEnum
from .printables import HmtImage, HmtText, Printable


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

    def __init__(self, printer: Escpos, localizer: HmtLocalizerEnum) -> None:
        self.printer = printer
        self.localizer = localizer.value(self.printer)

    @classmethod
    def from_conf(cls, conf: HmtConf) -> Hanmoto:
        printer_conf = conf.printer_conf
        printer_type = printer_conf.printer_type
        localizer = HmtLocalizerEnum.get_localizer(printer_conf.lang)
        if printer_type == HmtPrinterType.network:
            return cls.from_network(**printer_conf.conf.dict(), lang=localizer)
        elif printer_type == HmtPrinterType.dummy:
            return cls.from_dummy()
        else:
            raise HmtValueException(f"Unknown printer type: {printer_type}")

    @classmethod
    def from_network(
        cls,
        lang: HmtLocalizerEnum,
        host: str = "",
        port: int = 9100,
        timeout: int = 60,
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
        instance = cls(printer, lang)
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
        localizer = HmtLocalizerEnum.en
        instance = cls(printer, localizer)
        return instance

    def print_sequence(self, sequence: Iterable[Printable]) -> None:
        for elem in sequence:
            if isinstance(elem, HmtText):
                self.localizer.text(elem)
            elif isinstance(elem, HmtImage):
                image_src = elem.image_src
                self.printer.image(image_src, **elem.properties.dict())

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
