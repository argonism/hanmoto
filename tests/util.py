from pathlib import Path
from typing import List, Union

from hanmoto import Hanmoto, HmtPrinterConf, Printable
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
            if correct == len(included):
                break
    return len(included) == correct


def assert_printed_with_command(
    hmt: Hanmoto, printables: List[Printable], commands: List[bytes]
) -> None:
    with hmt:
        hmt.print_sequence(printables)
    assert include_list_with_order(hmt.printer._output_list, commands)
    hmt.printer.clear()
