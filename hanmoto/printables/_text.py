from __future__ import annotations

from pydantic import BaseModel

from hanmoto.exceptions import HmtValueException

from ._printable import PROPERTIES_TYPE, Printable


class HmtTextStyle(BaseModel):
    align: str = "left"
    font: int = 0
    bold: bool = False
    underline: int = 0
    smooth: bool = False
    width: int = 1
    height: int = 1
    density: int = 8
    invert: bool = False
    flip: bool = False
    double_width: bool = False
    double_height: bool = False
    custom_size: bool = False


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
    properties : HmtTextStyle, optional
        Dict that specify text style.
        see escpos/escpos.py#L624 for details.
    """

    def __init__(
        self, text: str, properties: HmtTextStyle = HmtTextStyle()
    ) -> None:
        self.text = text
        self.__properties: HmtTextStyle = properties
        super().__init__()

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HmtText):
            raise NotImplementedError()
        return self.text == __o.text and self.properties == __o.properties

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} properties={self.properties}>"

    @property
    def properties(self) -> HmtTextStyle:
        return self.__properties

    def center(self) -> HmtText:
        self.__properties.align = "center"
        return self

    def right(self) -> HmtText:
        self.__properties.align = "right"
        return self

    def left(self) -> HmtText:
        self.__properties.align = "left"
        return self

    def font_a(self) -> HmtText:
        self.__properties.font = 0
        return self

    def font_b(self) -> HmtText:
        self.__properties.font = 1
        return self

    def bold(self, bold: bool = True) -> HmtText:
        self.__properties.bold = bold
        return self

    def underline(self, underline: int = 1) -> HmtText:
        if not (0 <= underline <= 2):
            raise HmtValueException(
                "underline value must be 0 <= underline =< 2"
            )
        self.__properties.underline = underline
        return self

    def smooth(self, smooth: bool = True) -> HmtText:
        self.__properties.smooth = smooth
        return self

    def width(self, width: int = 1) -> HmtText:
        if not (1 <= width <= 8):
            raise HmtValueException("width value must be 1 <= height =< 8")
        self.__properties.width = width
        if width > 1:
            self.__properties.custom_size = True
        return self

    def height(self, height: int = 1) -> HmtText:
        if not (1 <= height <= 8):
            raise HmtValueException("height value must be 1 <= height =< 8")
        self.__properties.height = height
        if height > 1:
            self.__properties.custom_size = True
        return self

    def density(self, density: int = 8) -> HmtText:
        if not (0 <= density <= 8):
            raise HmtValueException("height value must be 0 <= height =< 8")
        self.__properties.density = density
        return self

    def invert(self, invert: bool = True) -> HmtText:
        self.__properties.invert = invert
        return self

    def flip(self, flip: bool = True) -> HmtText:
        self.__properties.flip = flip
        return self

    def double_width(self, double_width: bool = True) -> HmtText:
        self.__properties.double_width = double_width
        if double_width:
            self.__properties.custom_size = False

        return self

    def double_height(self, double_height: bool = True) -> HmtText:
        self.__properties.double_height = double_height
        if double_height:
            self.__properties.custom_size = False

        return self
