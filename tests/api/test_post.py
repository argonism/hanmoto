import base64
from io import BytesIO
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from pytest_mock import MockerFixture

from hanmoto import (
    HmtImage,
    HmtImageImpl,
    HmtImageStyle,
    HmtText,
    HmtTextStyle,
)
from hanmoto.api import app
from tests.api.fixtures import patch_printer
from tests.util import get_resource_path

client = TestClient(app)


def test_simple_text(patch_printer: MagicMock, mocker: MockerFixture) -> None:
    content = "This is a test.\nこんにちは！"
    response = client.post(
        "/print/text",
        json={
            "content": content,
        },
    )

    calls = [
        mocker.call.__enter__(),
        mocker.call.print_sequence([HmtText(content)]),
        mocker.call.__exit__(None, None, None),
    ]
    patch_printer.assert_has_calls(calls)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@pytest.mark.parametrize(
    "style",
    (
        HmtTextStyle(align="center"),
        HmtTextStyle(align="center", bold=True),
        HmtTextStyle(
            align="left",
            font=1,
            bold=True,
            underline=1,
            width=2,
            height=2,
            density=2,
            invert=True,
            flip=True,
            double_height=True,
            double_width=True,
        ),
    ),
)
def test_text_with_style(
    patch_printer: MagicMock, mocker: MockerFixture, style: HmtTextStyle
) -> None:
    content = "This is a test: test_text_with_style"
    response = client.post(
        "/print/text",
        json={
            "content": content,
            "style": style.dict(),
        },
    )

    calls = [
        mocker.call.__enter__(),
        mocker.call.print_sequence([HmtText(content, properties=style)]),
        mocker.call.__exit__(None, None, None),
    ]
    patch_printer.assert_has_calls(calls)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_simple_image_base64(
    patch_printer: MagicMock, mocker: MockerFixture
) -> None:
    img_path = get_resource_path("salt.png")
    base64_str = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    pil_image = Image.open(BytesIO(base64.b64decode(base64_str)))

    response = client.post(
        "/print/image",
        json={
            "base64": base64_str,
        },
    )
    calls = [
        mocker.call.__enter__(),
        mocker.call.print_sequence([HmtImage(pil_image)]),
        mocker.call.__exit__(None, None, None),
    ]
    patch_printer.assert_has_calls(calls)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@pytest.mark.parametrize(
    "style",
    (
        HmtImageStyle(center=True),
        HmtImageStyle(
            high_density_horizontal=True, high_density_vertical=True
        ),
        HmtImageStyle(
            center=True,
            impl=HmtImageImpl.bitImageRaster,
            high_density_horizontal=True,
            high_density_vertical=True,
            fragment_height=420,
        ),
    ),
)
def test_image_base64_with_style(
    patch_printer: MagicMock, mocker: MockerFixture, style: HmtImageStyle
) -> None:
    img_path = get_resource_path("salt.png")
    base64_str = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    pil_image = Image.open(BytesIO(base64.b64decode(base64_str)))

    response = client.post(
        "/print/image",
        json={"base64": base64_str, "style": style.dict()},
    )
    calls = [
        mocker.call.__enter__(),
        mocker.call.print_sequence([HmtImage(pil_image, properties=style)]),
        mocker.call.__exit__(None, None, None),
    ]
    patch_printer.assert_has_calls(calls)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_print_sequence(
    patch_printer: MagicMock, mocker: MockerFixture
) -> None:
    img_path = get_resource_path("salt.png")
    base64_str = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    pil_image = Image.open(BytesIO(base64.b64decode(base64_str)))

    response = client.post(
        "/print/image",
        json={"base64": base64_str, "style": style.dict()},
    )
    calls = [
        mocker.call.__enter__(),
        mocker.call.print_sequence([HmtImage(pil_image, properties=style)]),
        mocker.call.__exit__(None, None, None),
    ]
    patch_printer.assert_has_calls(calls)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
