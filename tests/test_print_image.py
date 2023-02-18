import unittest

from dotenv import load_dotenv

from tofu.printer import Tofu, TofuImage

load_dotenv()


class TestPrintImage(unittest.TestCase):
    def setUp(self) -> None:
        self.tofu = Tofu.get_instance()

    def test_upper(self) -> None:
        images = [
            TofuImage("tests/resource/Generate!!!.png"),
            TofuImage("tests/resource/salt.png"),
        ]
        with self.tofu:
            self.tofu.print_sequence(images)


if __name__ == "__main__":
    unittest.main()
