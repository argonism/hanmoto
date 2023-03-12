from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, unique

from escpos.printer import Escpos

from .exceptions import HmtValueException
from .printables import HmtText


class HmtLocalizer(ABC):
    @abstractmethod
    def __init__(self, printer: Escpos) -> None:
        ...

    @abstractmethod
    def text(self, text: HmtText) -> None:
        ...


class HmtLocalizerEn(HmtLocalizer):
    def __init__(self, printer: Escpos) -> None:
        self.printer = printer

    def text(self, text: HmtText) -> None:
        style_params = text.properties
        self.printer.set(**style_params.dict())
        text_str = text.text

        self.printer.text(text_str)
        self.printer.set()


class HmtLocalizerJp(HmtLocalizer):
    def __init__(self, printer: Escpos) -> None:
        self.printer = printer
        self.printer.charcode("CP932")
        self.printer._raw(b"\x1c\x43\x01")

    def text(self, text: HmtText) -> None:
        style_params = text.properties
        self.printer.set(**style_params.dict())
        text_str = text.text

        self.printer._raw(b"\x1c\x26")
        n = 0x00
        if style_params.double_width:
            n += 0x04
        if style_params.double_height:
            n += 0x08
        if n != 0x00:
            self.printer._raw(b"\x1c\x21" + n.to_bytes(1, byteorder="big"))

        self.printer._raw(text_str.encode("shift_jis", "ignore"))
        if n != 0x00:
            self.printer._raw(b"\x1c\x21\x00")
        self.printer._raw(b"\x1c\x2e")

        self.printer.set()


@unique
class HmtLocalizerEnum(Enum):
    en = HmtLocalizerEn
    jp = HmtLocalizerJp

    @classmethod
    def get_localizer(cls, lang: str) -> HmtLocalizerEnum:
        if lang in cls.__members__:
            return cls[lang]

        else:
            raise HmtValueException(f"localizer of {lang} is not defined")
