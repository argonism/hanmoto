import unittest

from dotenv import load_dotenv

from hanmoto import Hanmoto, HmtImage

load_dotenv()


class TestPrintImage(unittest.TestCase):
    def setUp(self) -> None:
        self.hmt = Hanmoto.from_network()

    def test_upper(self) -> None:
        images = [
            HmtImage("tests/resource/Generate!!!.png"),
            HmtImage("tests/resource/salt.png"),
        ]
        with self.hmt:
            self.hmt.print_sequence(images)


if __name__ == "__main__":
    unittest.main()
