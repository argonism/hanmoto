from pathlib import Path
from typing import Union

from hanmoto import HmtPrinterConf
from hanmoto.config import HmtConf, HmtPrinterType


def get_resource_dir() -> Path:
    return Path(__file__).parent.joinpath("resources")


def get_resource_path(file_path: Union[str, Path]) -> Path:
    return get_resource_dir().joinpath(file_path)


def create_test_hmtconf(lang: str = "en") -> HmtConf:
    printer_conf = HmtPrinterConf(printer_type=HmtPrinterType.dummy, lang=lang)
    return HmtConf(printer_conf=printer_conf)


def include_list_with_order(actual: list, included: list) -> bool:
    correct = 0
    for actual_elem in actual:
        if included[correct] == actual_elem:
            correct += 1
    return len(included) == correct
