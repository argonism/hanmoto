from typing import Generator
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from hanmoto.printer import (
    HmtConf,
    HmtDummyConf,
    HmtPrinterConf,
    HmtPrinterType,
)


def create_test_hmtconf() -> HmtConf:
    printer_conf = HmtPrinterConf(printer_type=HmtPrinterType.dummy)
    return HmtConf(printer_conf=printer_conf)


@pytest.fixture
def patch_printer(mocker: MockFixture) -> Generator[MagicMock, None, None]:
    mocked_printer = mocker.patch("hanmoto.api.printer")
    # mocked_printer = mocker.patch(
    #     "hanmoto.options.load_conf_from_cli", create_test_hmtconf
    # )

    mocked_printer.__enter__.side_effect = None
    yield mocked_printer
