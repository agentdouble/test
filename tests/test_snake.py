import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

PROJET_RACINE = Path(__file__).resolve().parents[1]
if str(PROJET_RACINE) not in sys.path:
    sys.path.insert(0, str(PROJET_RACINE))

from backend.snake import Snake


def test_snake_grows_three_segments_per_fruit():
    snake = Snake()
    initial_length = len(snake.positions)

    snake.manger()
    assert snake.grandir_restants == 3

    lengths = []
    for _ in range(3):
        assert snake.bouger() is True
        lengths.append(len(snake.positions))

    assert lengths == [initial_length + 1, initial_length + 2, initial_length + 3]
    assert snake.grandir_restants == 0

    assert snake.bouger() is True
    assert len(snake.positions) == initial_length + 3


def test_snake_growth_counter_accumulates():
    snake = Snake()
    initial_length = len(snake.positions)

    snake.manger()
    snake.manger()

    assert snake.grandir_restants == 6

    for step in range(6):
        assert snake.bouger() is True
        assert len(snake.positions) == initial_length + 1 + step

    assert snake.grandir_restants == 0

    assert snake.bouger() is True
    assert len(snake.positions) == initial_length + 6
