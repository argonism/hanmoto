from abc import abstractmethod
from enum import Enum
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel

from hanmoto.printer import Hanmoto, HmtImage, HmtText, Printable

load_dotenv()
app = FastAPI()

printer = Hanmoto.from_network()


class PrintableModel(BaseModel):
    @abstractmethod
    def to_hmt(self) -> Printable:
        raise NotImplementedError()


class TextStyle(BaseModel):
    align: str
    font: int
    bold: bool
    underline: int
    width: int
    height: int
    density: int
    invert: bool
    flip: bool
    double_width: int
    double_height: int


class TextModel(PrintableModel):
    content: str
    style: TextStyle = TextStyle(
        invert=False, flip=False, bold=False, underline=0
    )

    def to_hmt(self) -> Printable:
        return HmtText(self.content, properties=self.style.dict())


class ImageImpl(str, Enum):
    bitImageRaster = "bitImageRaster"
    graphics = "graphics"
    bitImageColumn = "bitImageColumn"


class ImageStyle(BaseModel):
    center: bool = False
    high_density_vertical: bool = False
    high_density_horizontal: bool = False
    impl: ImageImpl = ImageImpl.bitImageRaster
    fragment_height: int = 960


class ImageModel(PrintableModel):
    base64: str = ""
    image_src: str = ""
    style: ImageStyle = ImageStyle()

    def to_hmt(self) -> Printable:
        if self.base64:
            image = Image.open(self.base64)
        elif self.image_src:
            image = self.image_src
        return HmtImage(image, properties=self.style.dict())


class Sequence(BaseModel):
    contents: List[Printable]


@app.post("/print")
def print_text(sequence: Sequence) -> Dict[str, str]:
    with printer:
        for elem in sequence:
            properties = elem.style.dict()
            texts = [HmtText(text.content, properties=properties)]
            printer.print_sequence(texts)

    return {"status": "success"}
