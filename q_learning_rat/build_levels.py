

from q_learning_rat.model.level import Level
from q_learning_rat.model.position import Position

# level one
Level.builder(id=1, width=5, height=3) \
    .rat(Position(0, 0)) \
    .finish(Position(4, 2)) \
    .add_cheese(Position(0, 2)) \
    .add_cheese(Position(3, 1)) \
    .add_wall(Position(1, 2)) \
    .add_trap(Position(4, 0)) \
    .add_hole(Position(1, 0)) \
    .build() \
    .save(1)
