import urllib
from typing import Dict
import json


class TofuException(Exception):
    ...


class TofuValueException(TofuException):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class Printable(object):
    ...


class TofuText(Printable):
    def __init__(self, text: str) -> None:
        self.text = text
        self.properties: Dict[str, Union[bool, int]] = {}

    def bold(self, bold: bool = True) -> TofuText:
        self.properties["bold"] = bold
        return self

    def underline(self, underline: int = 1) -> TofuText:
        if not (0 <= underline <= 2):
            raise TofuValueException(
                "underline value must be 0 <= underline =< 2"
            )
        self.properties["underline"] = underline
        return self

    def invert(self, invert: bool = True) -> TofuText:
        self.properties["invert"] = invert
        return self

    def flip(self, flip: bool = True) -> TofuText:
        self.properties["flip"] = flip
        return self


class TofuClient(object):
    def __init__(self):
        self.target_host = "http://localhost:1885"

    def print_text(self, text: str) -> None:
        url = f"{self.target_host}/print_text/"
        data = {
            "content": text,
        }
        headers = {
            "Content-Type": "application/json",
        }

        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            print(body)
