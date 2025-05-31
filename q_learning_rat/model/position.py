from dataclasses import dataclass
from typing import Tuple

from q_learning_rat.model.move import Move


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def translate(self, move: Move) -> "Position":
        return Position(self.x + move.dx, self.y + move.dy)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y