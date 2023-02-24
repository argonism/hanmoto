import unittest

from dotenv import load_dotenv
from PIL import Image

from hanmoto import Hanmoto, HmtImage

load_dotenv()


class TestPrintImage(unittest.TestCase):
    def setUp(self) -> None:
        self.hmt = Hanmoto.from_network()

    def test_print_from_png(self) -> None:
        images = [
            HmtImage("tests/resource/Generate!!!.png"),
            HmtImage("tests/resource/salt.png"),
        ]
        with self.hmt:
            self.hmt.print_sequence(images)

    def test_print_from_PIL(self) -> None:
        generate_pil = Image.open("tests/resource/Generate!!!.png")
        salt_pil = Image.open("tests/resource/salt.png")
        images = [
            HmtImage(generate_pil),
            HmtImage(salt_pil),
        ]
        with self.hmt:
            self.hmt.print_sequence(images)


if __name__ == "__main__":
    unittest.main()
