from __future__ import annotations

from enum import Enum
from typing import Union

from PIL import Image
from pydantic import BaseModel

from ._printable import PROPERTIES_TYPE, Printable


class HmtImageImpl(str, Enum):
    bitImageRaster = "bitImageRaster"
    graphics = "graphics"
    bitImageColumn = "bitImageColumn"


class HmtImageStyle(BaseModel):
    center: bool = False
    high_density_vertical: bool = False
    high_density_horizontal: bool = False
    impl: HmtImageImpl = HmtImageImpl.bitImageRaster
    fragment_height: int = 960


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
    properties : HmtImageStyle, optional
        Dict that specify image style.
        see escpos/escpos.py#L123 for details.
    """

    def __init__(
        self,
        image_src: Union[str, Image.Image],
        properties: HmtImageStyle = HmtImageStyle(),
    ) -> None:
        self.image_src = image_src
        self.__properties: HmtImageStyle = properties
        super().__init__()

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HmtImage):
            raise NotImplementedError()
        return (
            self.image_src == __o.image_src
            and self.properties == __o.properties
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} properties={self.properties}>"

    @property
    def properties(self) -> HmtImageStyle:
        return self.__properties

    def high_density_vertical(self) -> HmtImage:
        self.__properties.high_density_vertical = True
        return self

    def high_density_horizontal(self) -> HmtImage:
        self.__properties.high_density_horizontal = True
        return self

    def bitImageRaster(self) -> HmtImage:
        self.__properties.impl = HmtImageImpl.bitImageRaster
        return self

    def graphics(self) -> HmtImage:
        self.__properties.impl = HmtImageImpl.graphics
        return self

    def bitImageColumn(self) -> HmtImage:
        self.__properties.impl = HmtImageImpl.bitImageColumn
        return self

    def fragment_height(self, height: int = 960) -> HmtImage:
        self.__properties.fragment_height = height
        return self

    def center(self) -> HmtImage:
        self.__properties.center = True
        return self
