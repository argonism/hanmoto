import unittest

from dotenv import load_dotenv

from hanmoto import PROPERTIES_TYPE, HmtText, HmtValueException

load_dotenv()


class TestHanmotoText(unittest.TestCase):
    def test_text(self) -> None:
        text = "dummy text"
        hmt_text = HmtText(text)
        self.assertEqual(hmt_text.text, text)
        properties: PROPERTIES_TYPE = {
            "align": "left",
            "font": 0,
            "bold": True,
            "underline": 2,
            "width": 8,
            "height": 7,
            "density": 7,
            "invert": True,
            "flip": True,
            "double_width": True,
            "double_height": True,
        }
        hmt_text = HmtText(text, properties=properties)
        self.assertEqual(hmt_text.properties, properties)

    def test_text_align(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.center()
        self.assertEqual(hmt_text.properties["align"], "center")
        hmt_text = hmt_text.right()
        self.assertEqual(hmt_text.properties["align"], "right")
        hmt_text = hmt_text.left()
        self.assertEqual(hmt_text.properties["align"], "left")

    def test_text_font(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.font_a()
        self.assertEqual(hmt_text.properties["font"], 0)
        hmt_text = hmt_text.font_b()
        self.assertEqual(hmt_text.properties["font"], 1)

    def test_text_bold(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.bold()
        self.assertEqual(hmt_text.properties["bold"], True)
        hmt_text = hmt_text.bold(False)
        self.assertEqual(hmt_text.properties["bold"], False)

    def test_text_underline(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.underline()
        self.assertEqual(hmt_text.properties["underline"], 1)
        for i in range(3):
            hmt_text = hmt_text.underline(i)
            self.assertEqual(hmt_text.properties["underline"], i)
        self.assertRaises(HmtValueException, lambda: hmt_text.underline(3))
        self.assertRaises(HmtValueException, lambda: hmt_text.underline(-1))

    def test_text_width(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.width()
        self.assertEqual(hmt_text.properties["width"], 1)
        for i in range(1, 9):
            hmt_text = hmt_text.width(i)
            self.assertEqual(hmt_text.properties["width"], i)
        self.assertRaises(HmtValueException, lambda: hmt_text.width(9))
        self.assertRaises(HmtValueException, lambda: hmt_text.width(0))

    def test_text_height(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.height()
        self.assertEqual(hmt_text.properties["height"], 1)
        for i in range(1, 9):
            hmt_text = hmt_text.height(i)
            self.assertEqual(hmt_text.properties["height"], i)
        self.assertRaises(HmtValueException, lambda: hmt_text.height(9))
        self.assertRaises(HmtValueException, lambda: hmt_text.height(0))

    def test_text_density(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.density()
        self.assertEqual(hmt_text.properties["density"], 8)
        for i in range(9):
            hmt_text = hmt_text.density(i)
            self.assertEqual(hmt_text.properties["density"], i)
        self.assertRaises(HmtValueException, lambda: hmt_text.density(9))
        self.assertRaises(HmtValueException, lambda: hmt_text.density(-1))

    def test_text_invert(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.invert()
        self.assertEqual(hmt_text.properties["invert"], True)
        hmt_text = hmt_text.invert(False)
        self.assertEqual(hmt_text.properties["invert"], False)

    def test_text_flip(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.flip()
        self.assertEqual(hmt_text.properties["flip"], True)
        hmt_text = hmt_text.flip(False)
        self.assertEqual(hmt_text.properties["flip"], False)

    def test_text_double_width(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.double_width()
        self.assertEqual(hmt_text.properties["double_width"], True)
        hmt_text = hmt_text.double_width(False)
        self.assertEqual(hmt_text.properties["double_width"], False)

    def test_text_double_height(self) -> None:
        text = "text"
        hmt_text = HmtText(text)
        hmt_text = hmt_text.double_height()
        self.assertEqual(hmt_text.properties["double_height"], True)
        hmt_text = hmt_text.double_height(False)
        self.assertEqual(hmt_text.properties["double_height"], False)


if __name__ == "__main__":
    unittest.main()
