from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture, MockFixture

from hanmoto import Hanmoto, HmtImage
from tests.hanmoto.fixtures import patched_escpos_printer
from tests.util import (
    create_test_hmtconf,
    get_resource_path,
    include_list_with_order,
)


@pytest.fixture
def patched_hmt(mocker: MockFixture) -> Hanmoto:
    conf = create_test_hmtconf()
    htm = Hanmoto.from_conf(conf)

    htm.printer = mocker.patch("escpos.printer.Escpos")
    return htm


def test_print_style(patched_hmt: Hanmoto, mocker: MockerFixture) -> None:
    image_src = Path("salt.png").absolute()
    hmt_image = HmtImage(get_resource_path(image_src))
    with patched_hmt:
        patched_hmt.print_sequence([hmt_image])

    calls = [
        mocker.call.image(image_src, **hmt_image.properties.dict()),
        mocker.call.cut(),
    ]
    patched_hmt.printer.assert_has_calls(calls)
