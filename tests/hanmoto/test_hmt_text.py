from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture, MockFixture

from hanmoto import HmtText, HmtTextStyle
from tests.hanmoto import patch_escpos

# def test_simple_text(patch_escpos: MagicMock, mocker: MockerFixture) -> None:
#     content = ""
#     text = HmtText(
#         content
#     )

#     printer.

#     patch_printer.assert_has_calls(calls)
#     assert response.status_code == 200
#     assert response.json() == {"status": "success"}
