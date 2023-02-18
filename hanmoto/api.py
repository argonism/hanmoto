from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from hanmoto.printer import Hanmoto, HmtText

load_dotenv()
app = FastAPI()

printer = Hanmoto.from_network()


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


class Text(BaseModel):
    content: str
    style: TextStyle = TextStyle(
        invert=False, flip=False, bold=False, underline=0
    )


@app.post("/print_text/")
def print_text(text: Text) -> Dict[str, str]:
    with printer:
        properties = text.style.dict()
        texts = [HmtText(text.content, properties=properties)]
        printer.print_sequence(texts)

    return {"status": "success"}
