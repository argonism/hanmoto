from typing import Generator

import pytest
from pytest_mock import MockFixture

from hanmoto import Hanmoto
from tests.util import create_test_hmtconf


@pytest.fixture
def patched_escpos_printer(
    mocker: MockFixture,
) -> Generator[Hanmoto, None, None]:
    mocked_escpos = mocker.patch("hanmoto.printer.Hanmoto")

    yield mocked_escpos


@pytest.fixture
def dummy_hmt() -> Hanmoto:
    conf = create_test_hmtconf()
    printer = Hanmoto.from_conf(conf)
    return printer
