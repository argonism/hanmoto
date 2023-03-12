from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class HmtPrinterType(Enum):
    network = "network"
    dummy = "dummy"

    @classmethod
    def get_types(cls) -> list:
        return [i.name for i in cls]


class HmtPrinterTypeConf(BaseModel):
    ...


class HmtNetworkConf(HmtPrinterTypeConf):
    host: str = ""
    port: int = 9100
    timeout: int = 60


class HmtDummyConf(HmtPrinterTypeConf):
    ...


class HmtPrinterConf(BaseModel):
    printer_type: HmtPrinterType = HmtPrinterType.network
    conf: HmtPrinterTypeConf = HmtPrinterTypeConf()
    lang: str = "en"


class HmtApiConf(BaseModel):
    api_host: str = "127.0.0.1"
    port: int = 10020
    reload: bool = False


class HmtConf(BaseModel):
    printer_conf: HmtPrinterConf = HmtPrinterConf()
    api_conf: HmtApiConf = HmtApiConf()
