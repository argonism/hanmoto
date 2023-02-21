from __future__ import annotations

from typing import Union

from PIL import Image

from ._printable import PROPERTIES_TYPE, Printable


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
        see escpos/escpos.py#L123 for details.
    """

    def __init__(
        self,
        image_src: Union[str, Image.Image],
        properties: PROPERTIES_TYPE = {},
    ) -> None:
        self.image_src = image_src
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
