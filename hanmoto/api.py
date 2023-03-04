import base64
from abc import abstractmethod
from io import BytesIO
from typing import Dict, List, Literal, Optional, Union

from dotenv import load_dotenv
from fastapi import FastAPI, Request
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
from hanmoto.exceptions import (
    HmtValueException,
    HmtWebAPIException,
    HmtWebAPISequenceException,
)
from hanmoto.printer import HmtConf


class Settings(BaseSettings):
    app_name: str = "net"
    net_host: str = ""


load_dotenv()

printer: Hanmoto


def load_app(conf: HmtConf) -> FastAPI:
    global printer
    app = FastAPI()
    setup_app(app)
    printer = Hanmoto.from_conf(conf)
    return app


class PrintableModel(BaseModel):
    @abstractmethod
    def to_hmt(self) -> Printable:
        raise NotImplementedError()


class TextModel(PrintableModel):
    type: Literal["text"] = "text"
    content: str
    style: Optional[HmtTextStyle] = None

    def to_hmt(self) -> Printable:
        if self.style is None:
            return HmtText(self.content)
        else:
            return HmtText(self.content, properties=self.style)


class ImageModel(PrintableModel):
    type: Literal["image"] = "image"
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
            raise HmtValueException("Specify image source")
        return HmtImage(image, properties=self.style)


class Sequence(BaseModel):
    contents: List[Union[ImageModel, TextModel]]


def setup_app(app: FastAPI) -> None:
    @app.post("/print/sequence")
    async def print_sequence(
        sequence: Sequence, request: Request
    ) -> Dict[str, str]:
        def validate_sequence(sequence_list: List[Dict]) -> None:
            for i, content in enumerate(sequence_list):
                if "type" not in content:
                    raise HmtWebAPISequenceException(
                        (
                            f"content: {content} (at index {i}) has no 'type' field. "
                            "Please specify type field for all content in 'contents'. "
                            "e.g. '{{'type': 'text', 'content': 'string'}}'"
                        )
                    )

        body = await request.json()
        validate_sequence(body["contents"])

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
