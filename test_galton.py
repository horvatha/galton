from collections import Counter
from enum import Enum, auto
from fractions import Fraction

from galton import Galton


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


def constant_direction(direction: Direction):
    move_dict = {
        Direction.LEFT: Fraction(-1, 2),
        Direction.RIGHT: Fraction(1, 2),
    }

    def random_direction():
        return move_dict[direction]
    return random_direction


def test_left_bin_left_direction():
    galton = Galton(
        row_pairs=1,
        bins=2,
        random_bin=lambda bins: 1,
        random_direction=constant_direction(Direction.LEFT),
    )
    result = galton.simulate(beads=100_000, start=None)
    assert result == Counter([1] * 100_000)


def test_left_bin_right_direction():
    galton = Galton(
        row_pairs=1,
        bins=2,
        random_bin=lambda bins: 1,
        random_direction=constant_direction(Direction.RIGHT),
    )
    result = galton.simulate(beads=100_000, start=None)
    assert result == Counter([2] * 100_000)
