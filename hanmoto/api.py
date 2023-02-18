from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from hanmoto.printer import Hanmoto, HmtText

load_dotenv()
app = FastAPI()

printer = Hanmoto.from_network()


class PrintStyle(BaseModel):
    invert: bool
    flip: bool
    bold: bool
    underline: int


class PrintText(BaseModel):
    content: str
    style: PrintStyle = PrintStyle(
        invert=False, flip=False, bold=False, underline=0
    )


@app.post("/print_text/")
def print_text(text: PrintText) -> Dict[str, str]:
    with printer:
        properties = text.style.dict()
        texts = [HmtText(text.content, properties=properties)]
        printer.print_sequence(texts)

    return {"status": "success"}
