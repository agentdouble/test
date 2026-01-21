import unittest
from pathlib import Path


class TestSnakeColor(unittest.TestCase):
    def test_snake_color_is_orange(self):
        source = (Path(__file__).parent / "backend" / "snake.py").read_text()
        self.assertIn('identifiant="orange"', source)
        self.assertIn("couleurs=((255, 165, 0),)", source)


if __name__ == "__main__":
    unittest.main()
