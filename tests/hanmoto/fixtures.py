from typing import Generator
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from hanmoto import Hanmoto


@pytest.fixture
def patched_escpos_printer(
    mocker: MockFixture,
) -> Generator[Hanmoto, None, None]:
    mocked_escpos = mocker.patch("hanmoto.printer.Hanmoto")

    yield mocked_escpos
