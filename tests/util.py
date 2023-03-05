from pathlib import Path

from hanmoto import HmtPrinterConf
from hanmoto.config import HmtConf, HmtPrinterType


def get_resource_dir() -> Path:
    return Path(__file__).parent.joinpath("resources")


def get_resource_path(file_path: str) -> Path:
    return get_resource_dir().joinpath(file_path)


def create_test_hmtconf() -> HmtConf:
    printer_conf = HmtPrinterConf(printer_type=HmtPrinterType.dummy)
    return HmtConf(printer_conf=printer_conf)
