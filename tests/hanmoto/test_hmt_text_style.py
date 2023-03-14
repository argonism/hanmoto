import pytest

from hanmoto import Hanmoto, HmtText
from hanmoto.exceptions import HmtValueException
from tests.util import assert_printed_with_command, create_test_hmtconf


@pytest.fixture
def dummy_hmt() -> Hanmoto:
    conf = create_test_hmtconf()
    printer = Hanmoto.from_conf(conf)
    return printer


def test_text_style_align(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)
    assert hmt_text.properties.align == "left"
    expected = [b"\x1ba\x00"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.center()
    assert hmt_text.properties.align == "center"
    expected = [b"\x1ba\x01"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.right()
    assert hmt_text.properties.align == "right"
    expected = [b"\x1ba\x02"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)


def test_text_style_font(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    assert hmt_text.properties.font == 0
    expected = [b"\x1bM\x00"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.font_b()
    assert hmt_text.properties.font == 1
    expected = [b"\x1bM\x01"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)


def test_text_style_bold(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    assert not hmt_text.properties.bold
    expected = [b"\x1bE\x00"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.bold()
    assert hmt_text.properties.bold
    expected = [b"\x1bE\x01"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)


def test_text_style_underline(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    for i in range(3):
        hmt_text.underline(i)
        assert hmt_text.properties.underline == i
        expected = [b"\x1b-" + bytes([i])]
        assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    with pytest.raises(HmtValueException):
        hmt_text.underline(3)

    with pytest.raises(HmtValueException):
        hmt_text.underline(-1)


def test_text_style_smooth(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    assert not hmt_text.properties.smooth
    expected = [b"\x1db\x00"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.smooth()
    assert hmt_text.properties.smooth
    expected = [b"\x1db\x01"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)


def test_text_style_width(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    for i in range(1, 9):
        hmt_text.width(i)
        assert hmt_text.properties.width == i
        if i > 1:
            assert hmt_text.properties.custom_size
            expected = [b"\x1d!" + bytes([(i - 1) * 16])]
            assert_printed_with_command(dummy_hmt, [hmt_text], expected)
        else:
            assert not hmt_text.properties.custom_size
            expected = [b"\x1b!\x00", b"\x1b!\x00\x1b!\x00"]
            assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.width(1)
    assert hmt_text.properties.width == 1
    assert not hmt_text.properties.custom_size

    with pytest.raises(HmtValueException):
        hmt_text.width(9)

    with pytest.raises(HmtValueException):
        hmt_text.width(0)


def test_text_style_height(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)

    for i in range(1, 9):
        hmt_text.height(i)
        assert hmt_text.properties.height == i
        if i > 1:
            assert hmt_text.properties.custom_size
            expected = [b"\x1d!" + bytes([(i - 1)])]
            assert_printed_with_command(dummy_hmt, [hmt_text], expected)
        else:
            assert not hmt_text.properties.custom_size
            expected = [b"\x1b!\x00", b"\x1b!\x00\x1b!\x00"]
            assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.height(1)
    assert hmt_text.properties.height == 1
    assert not hmt_text.properties.custom_size

    with pytest.raises(HmtValueException):
        hmt_text.height(9)

    with pytest.raises(HmtValueException):
        hmt_text.height(0)


def test_text_style_invert(dummy_hmt: Hanmoto) -> None:
    text_content = "test_text_style"
    hmt_text = HmtText(text_content)
    assert not hmt_text.properties.invert
    expected = [b"\x1dB\x00"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)

    hmt_text.invert()
    assert hmt_text.properties.invert
    expected = [b"\x1dB\x01"]
    assert_printed_with_command(dummy_hmt, [hmt_text], expected)
