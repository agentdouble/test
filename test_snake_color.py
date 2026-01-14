import unittest
from pathlib import Path


class TestSnakeColor(unittest.TestCase):
    def test_snake_color_is_orange(self):
        source = Path(__file__).with_name("snake.py").read_text()
        self.assertIn("ORANGE", source)
        self.assertIn("couleur = ORANGE", source)


if __name__ == "__main__":
    unittest.main()
