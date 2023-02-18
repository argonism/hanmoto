from __future__ import annotations

from hanmoto.exceptions import HmtValueException
from hanmoto.printables import PROPERTIES_TYPE, Printable


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
        see escpos/escpos.py#L624 for details.
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
