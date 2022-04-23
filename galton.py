from collections import Counter
from typing import Callable
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
from pandas import Series
import random

RandomFactory = Callable[[], Callable[[int, int], int]]


class Galton:
    """
    A Galton board class that can be used to simulate the distribution into
    bins of a number of beads running through the board.

    The board is assumed to comprise an even number of 'row pairs'. Whenever a
    bead passes through a member of a row pair in a simulated run, the bin
    position of the bead is moved randomly either a half-bin unit to the
    left or to the right. Consequently, after passing a row pair, the bin
    position of the bead has either moved a full bin unit to the left, stayed
    at the same bin unit, or moved a full bin unit to the right. If this
    results in a bin position outside the board, the bead is bounced back into
    the board by one full bin unit.
    """
    def __init__(
            self,
            row_pairs: int,
            bins: int, *,
            random_position_factory: RandomFactory = lambda: random.randint,
            random_direction_factory: RandomFactory = lambda: random.randint
    ):
        """
        Initialize a Galton board with the specified number of row pairs and bins.

        Arguments
        --------
        row_pairs: int
            The number of "row pairs"
        bins: int
            The number of bins (zero is not included as a bin)
        """
        self.bins = bins
        self.rows = row_pairs * 2
        self.random_position = random_position_factory()
        self.random_direction = random_direction_factory()

    def is_valid(self, position: float) -> bool:
        """
        Check if the argument is a valid board position.

        Argument
        --------
        position: float
            The position value to be checked (in bin units, including
            half-bins)

        Returns
        -------
        check: bool
            True if the position value is valid, or false otherwise
        """
        return 0 < position < self.bins + 1

    def move_down(self, position: float) -> float:
        """
        Move the bead down one row on the board by updating its bin position.

        Argument
        --------
        position: float
            The current position of the bead (in bin units, including
            half-bins)

        Returns
        -------
        position: float
            The new position of the bead after passing a row (in bin units,
            including half-bins)
        """
        d = -0.5 if self.random_direction(0, 1) else 0.5
        position += d
        if not self.is_valid(position):
            position -= d * 2
        return position

    def run_bead(self, start=None) -> int:
        """
        Run a bead from its starting position into a final bin by passing it
        through the board.

        Argument
        --------
        start:
            The starting position of the bead (see `simulate()` for details)

        Returns
        -------
        position: int
            The bin in which the bead ends up after running through the board
        """
        position = start or self.random_position(1, self.bins)
        if not self.is_valid(position):
            raise ValueError("Bin position out of range")
        for _ in range(self.rows):
            position = self.move_down(position)
        return int(position)

    def simulate(self, beads: int, start=None) -> None:
        """
        Show the histogram of results for a specified number of beads on the
        board.

        The simulation condition can be specified by specifying the `start`
        argument (see below).

        Arguments
        ---------
        beads: int
            The number of beads that will be used in the simulation
        start: int, or None
            If `start` is an integer, its value is used by as the starting bin
                    position of every bead. If `start` is None (the default), the
            starting bin position of each bead will be randomly chosen from the
            possible bin positions of the board.
        """
        count = Counter(self.run_bead(start) for _ in range(beads))

        (Series(count).sort_index()
                      .mul(100)
                      .div(beads)
                      .plot(kind="bar",
                            xlabel="Bins",
                            ylabel="Relative frequency"))

        plt.xticks(rotation=0)
        plt.gca().yaxis.set_major_formatter(PercentFormatter())
        plt.show()

# Simulate a classic Galton board in which all beads are released at the
# midpoint of the board:
Galton(row_pairs=11, bins=21).simulate(beads=100000, start=11)

# Simulate the variant used in the YouTube show in which any starting position
# is possible:
Galton(row_pairs=11, bins=21).simulate(beads=100000, start=None)
