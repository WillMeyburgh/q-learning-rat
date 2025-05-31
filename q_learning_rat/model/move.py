from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    dx: int
    dy: int
    action: int

    def __hash__(self):
        return hash((self.dx, self.dy))
    
    def __eq__(self, other):
        return self.dx == other.dx and self.dy == other.dy
    
    @classmethod
    def left(cls) -> "Move":
        return Move(dx=-1, dy=0, action=0)
    
    @classmethod
    def right(cls) -> "Move":
        return Move(dx=1, dy=0, action=1)
    
    @classmethod
    def up(cls) -> "Move":
        return Move(dx=0, dy=1, action=2)
    
    @classmethod
    def down(cls) -> "Move":
        return Move(dx=0, dy=-1, action=3)
    
    @classmethod
    def from_action(cls, action: int) -> "Move":
        if action == 0:
            return cls.left()
        elif action == 1:
            return cls.right()
        elif action == 2:
            return cls.up()
        elif action == 3:
            return cls.down()