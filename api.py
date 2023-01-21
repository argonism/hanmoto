from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from tofu import Tofu

load_dotenv()
app = FastAPI()
tofu = Tofu.get_instance()


class PrintText(BaseModel):
    content: str


@app.post("/print_text/")
def print_text(text: PrintText) -> Dict[str, str]:
    with tofu:
        tofu.text(text.content)

    return {"status": "success"}
