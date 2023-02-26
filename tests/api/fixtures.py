from typing import Generator
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture


@pytest.fixture
def patch_printer(mocker: MockFixture) -> Generator[MagicMock, None, None]:
    # mocked_printer = mocker.patch("hanmoto.api.printer")
    mocked_printer = mocker.patch("hanmoto.options.load_conf_from_cli")

    mocked_printer.__enter__.side_effect = None
    yield mocked_printer
