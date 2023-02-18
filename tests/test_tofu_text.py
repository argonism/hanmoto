import unittest

from dotenv import load_dotenv

from tofu.printer import Tofu, TofuText, TofuValueException

load_dotenv()


class TestTofuText(unittest.TestCase):
    def test_text(self) -> None:
        text = "dummy text"
        tofu_text = TofuText(text)
        self.assertEqual(tofu_text.text, text)

    def test_text_align(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.center()
        self.assertEqual(tofu_text.properties["align"], "center")
        tofu_text = tofu_text.right()
        self.assertEqual(tofu_text.properties["align"], "right")
        tofu_text = tofu_text.left()
        self.assertEqual(tofu_text.properties["align"], "left")

    def test_text_font(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.font_a()
        self.assertEqual(tofu_text.properties["font"], 0)
        tofu_text = tofu_text.font_b()
        self.assertEqual(tofu_text.properties["font"], 1)

    def test_text_bold(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.bold()
        self.assertEqual(tofu_text.properties["bold"], True)
        tofu_text = tofu_text.bold(False)
        self.assertEqual(tofu_text.properties["bold"], False)

    def test_text_underline(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.underline()
        self.assertEqual(tofu_text.properties["underline"], 1)
        for i in range(3):
            tofu_text = tofu_text.underline(i)
            self.assertEqual(tofu_text.properties["underline"], i)
        self.assertRaises(TofuValueException, lambda: tofu_text.underline(3))
        self.assertRaises(TofuValueException, lambda: tofu_text.underline(-1))

    def test_text_width(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.width()
        self.assertEqual(tofu_text.properties["width"], 1)
        for i in range(1, 9):
            tofu_text = tofu_text.width(i)
            self.assertEqual(tofu_text.properties["width"], i)
        self.assertRaises(TofuValueException, lambda: tofu_text.width(9))
        self.assertRaises(TofuValueException, lambda: tofu_text.width(0))

    def test_text_height(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.height()
        self.assertEqual(tofu_text.properties["height"], 1)
        for i in range(1, 9):
            tofu_text = tofu_text.height(i)
            self.assertEqual(tofu_text.properties["height"], i)
        self.assertRaises(TofuValueException, lambda: tofu_text.height(9))
        self.assertRaises(TofuValueException, lambda: tofu_text.height(0))

    def test_text_density(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.density()
        self.assertEqual(tofu_text.properties["density"], 8)
        for i in range(9):
            tofu_text = tofu_text.density(i)
            self.assertEqual(tofu_text.properties["density"], i)
        self.assertRaises(TofuValueException, lambda: tofu_text.density(9))
        self.assertRaises(TofuValueException, lambda: tofu_text.density(-1))

    def test_text_invert(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.invert()
        self.assertEqual(tofu_text.properties["invert"], True)
        tofu_text = tofu_text.invert(False)
        self.assertEqual(tofu_text.properties["invert"], False)

    def test_text_flip(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.flip()
        self.assertEqual(tofu_text.properties["flip"], True)
        tofu_text = tofu_text.flip(False)
        self.assertEqual(tofu_text.properties["flip"], False)

    def test_text_double_width(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.double_width()
        self.assertEqual(tofu_text.properties["double_width"], True)
        tofu_text = tofu_text.double_width(False)
        self.assertEqual(tofu_text.properties["double_width"], False)

    def test_text_double_height(self) -> None:
        text = "text"
        tofu_text = TofuText(text)
        tofu_text = tofu_text.double_height()
        self.assertEqual(tofu_text.properties["double_height"], True)
        tofu_text = tofu_text.double_height(False)
        self.assertEqual(tofu_text.properties["double_height"], False)


if __name__ == "__main__":
    unittest.main()
