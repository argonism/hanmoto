import base64

from fastapi.testclient import TestClient

from hanmoto.api import app
from tests.util import get_resource

client = TestClient(app)


def test_simple_text() -> None:
    response = client.post(
        "/print/text",
        json={
            "content": "This is a test.\nこんにちは！",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_simple_image_base64() -> None:
    img_path = get_resource("salt.png")
    base64_str = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    print(base64_str)
    response = client.post(
        "/print/image",
        json={
            "base64": base64_str,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


# def test_create_existing_item() -> None:
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "The Foo ID Stealers",
#             "description": "There goes my stealer",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Item already exists"}
