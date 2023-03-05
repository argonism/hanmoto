from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture, MockFixture

from hanmoto import Hanmoto, HmtText
from tests.hanmoto.fixtures import patched_escpos_printer
from tests.util import create_test_hmtconf


@pytest.fixture
def dummy_hmt() -> Hanmoto:
    conf = create_test_hmtconf()
    printer = Hanmoto.from_conf(conf)
    return printer


def test_simple_text(
    patched_escpos_printer: MagicMock, dummy_hmt: Hanmoto
) -> None:
    texts = [HmtText("test from test_simple_text")]
    with dummy_hmt:
        dummy_hmt.print_sequence(texts)

    assert patched_escpos_printer.call_args == ""
