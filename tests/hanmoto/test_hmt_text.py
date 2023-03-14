from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest
from pytest_mock import MockerFixture, MockFixture

from hanmoto import Hanmoto, HmtText
from tests.hanmoto.fixtures import patched_escpos_printer
from tests.util import create_test_hmtconf, include_list_with_order


@pytest.fixture
def dummy_hmt(request: FixtureRequest) -> Hanmoto:
    conf = create_test_hmtconf(request.param)
    printer = Hanmoto.from_conf(conf)
    return printer


@pytest.mark.parametrize("dummy_hmt", ["en"], indirect=True)
def test_text_style(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"

    print_expected = [
        b"\x1b!\x00",  # ESC ! 0 (font as 1)
        b"\x1b!\x00\x1b!\x00",  # ESC ! 0 ESC ! 0 (specify normal font size)
        b"\x1b{\x01",  # ESC { 1 (flip)
        b"\x1db\x01",  # GS b 1 (smoothing)
        b"\x1bE\x01",  # ESC E 1 (bold)
        b"\x1b-\x01",  # ESC - 1 (underline)
        b"\x1bM\x01",  # ESC M 1 (specify font B)
        b"\x1ba\x01",  # ESC a 1 (specify text align as center)
        b"\x1d|\x04",  # GS | 4 (specify density) * this ESC/POS commands does not found in epson ESC/POS reference.
        b"\x1dB\x01",  # GS B 1 (invert)
        b"\x1bt\x00",  # ESC t 0 (code page 0)
        text_content.encode("cp437", "ignore"),
    ]
    text = (
        HmtText(text_content)
        .flip()
        .smooth()
        .bold()
        .underline(1)
        .font_b()
        .center()
        .density(4)
        .invert()
    )
    with dummy_hmt:
        dummy_hmt.print_sequence([text])

        assert dummy_hmt.printer._output_list == print_expected


@pytest.mark.parametrize("dummy_hmt", ["jp"], indirect=True)
def test_jp_text(dummy_hmt: Hanmoto) -> None:
    text_content = "日本語テスト from test_jp_text"
    init_expected = [
        b"\x1bt\x01",  # ESC t 1 (specify code page as 1 (katakana))
        b"\x1c\x43\x02",  # FS C 2 (specify Shift_JIS-2004)
    ]

    assert dummy_hmt.printer._output_list == init_expected
    dummy_hmt.printer.clear()

    print_expected = [
        b"\x1c&",  # activate kanji mode
        text_content.encode("sjis_2004", "ignore"),
        b"\x1c.",  # deactivate kanji mode
    ]
    text = HmtText(text_content)
    with dummy_hmt:
        dummy_hmt.print_sequence([text])

        assert include_list_with_order(
            dummy_hmt.printer._output_list, print_expected
        )
