import unittest
from pathlib import Path


class TestSnakeColor(unittest.TestCase):
    def test_snake_color_is_gray(self):
        source = Path(__file__).with_name("snake.py").read_text()
        self.assertIn("GRIS_CLAIR", source)
        self.assertIn("couleur = GRIS_CLAIR", source)


if __name__ == "__main__":
    unittest.main()
