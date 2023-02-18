from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from tofu.printer import Tofu, TofuText

load_dotenv()
app = FastAPI()


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
    tofu = Tofu.get_instance()
    with tofu:
        texts = [TofuText(text.content)]
        tofu.print_sequence(texts)

    return {"status": "success"}
