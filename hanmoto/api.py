import base64
from abc import abstractmethod
from io import BytesIO
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel, BaseSettings

from hanmoto import (
    Hanmoto,
    HmtImage,
    HmtImageStyle,
    HmtText,
    HmtTextStyle,
    Printable,
)
from hanmoto.options import load_conf_from_cli
from hanmoto.printer import HmtConf


class Settings(BaseSettings):
    app_name: str = "net"
    net_host: str = ""


load_dotenv()
app = FastAPI()
hmt_conf = load_conf_from_cli()

printer: Hanmoto


@app.on_event("startup")
async def startup_event() -> None:
    global printer
    printer = Hanmoto.from_conf(hmt_conf)


class PrintableModel(BaseModel):
    @abstractmethod
    def to_hmt(self) -> Printable:
        raise NotImplementedError()


class TextModel(PrintableModel):
    content: str
    style: HmtTextStyle = HmtTextStyle()

    def to_hmt(self) -> Printable:
        return HmtText(self.content, properties=self.style)


class ImageModel(PrintableModel):
    base64: str = ""
    image_src: str = ""
    style: HmtImageStyle = HmtImageStyle()

    def to_hmt(self) -> Printable:
        if self.base64:
            img_base64_bytes = base64.b64decode(self.base64)
            image = Image.open(BytesIO(img_base64_bytes))
        elif self.image_src:
            image = self.image_src
        else:
            raise Exception("")
        return HmtImage(image, properties=self.style)


class Sequence(BaseModel):
    contents: List[PrintableModel]


@app.post("/print/sequence")
def print_sequence(sequence: Sequence) -> Dict[str, str]:
    with printer:
        printables = [elem.to_hmt() for elem in sequence.contents]
        printer.print_sequence(printables)

    return {"status": "success"}


@app.post("/print/text")
def print_text(text: TextModel) -> Dict[str, str]:
    with printer:
        printer.print_sequence([text.to_hmt()])

    return {"status": "success"}


@app.post("/print/image")
def print_image(image: ImageModel) -> Dict[str, str]:
    with printer:
        printer.print_sequence([image.to_hmt()])

    return {"status": "success"}
