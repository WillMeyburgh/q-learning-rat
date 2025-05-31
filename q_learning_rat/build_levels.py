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

# level two
Level.builder(id=2, width=7, height=5) \
    .rat(Position(0, 0)) \
    .finish(Position(6, 4)) \
    .add_cheese(Position(0, 4)) \
    .add_cheese(Position(3, 1)) \
    .add_cheese(Position(5, 3)) \
    .add_wall(Position(1, 2)) \
    .add_wall(Position(5, 2)) \
    .add_trap(Position(4, 0)) \
    .add_trap(Position(2, 3)) \
    .add_hole(Position(1, 0)) \
    .add_hole(Position(3, 4)) \
    .build() \
    .save(2)

# level three
Level.builder(id=3, width=9, height=7) \
    .rat(Position(0, 0)) \
    .finish(Position(8, 6)) \
    .add_cheese(Position(0, 6)) \
    .add_cheese(Position(4, 1)) \
    .add_cheese(Position(7, 3)) \
    .add_wall(Position(2, 2)) \
    .add_wall(Position(6, 2)) \
    .add_trap(Position(5, 0)) \
    .add_trap(Position(3, 5)) \
    .add_hole(Position(1, 1)) \
    .add_hole(Position(4, 4)) \
    .build() \
    .save(3)

# level four
Level.builder(id=4, width=11, height=9) \
    .rat(Position(0, 0)) \
    .finish(Position(10, 8)) \
    .add_cheese(Position(0, 8)) \
    .add_cheese(Position(5, 1)) \
    .add_cheese(Position(8, 3)) \
    .add_wall(Position(3, 2)) \
    .add_wall(Position(7, 2)) \
    .add_trap(Position(6, 0)) \
    .add_trap(Position(4, 5)) \
    .add_hole(Position(1, 1)) \
    .add_hole(Position(5, 4)) \
    .build() \
    .save(4)

# level five
Level.builder(id=5, width=6, height=4) \
    .rat(Position(0, 0)) \
    .finish(Position(5, 3)) \
    .add_cheese(Position(0, 3)) \
    .add_cheese(Position(3, 1)) \
    .add_wall(Position(1, 2)) \
    .add_trap(Position(4, 0)) \
    .add_hole(Position(1, 0)) \
    .build() \
    .save(5)

# level six
Level.builder(id=6, width=8, height=6) \
    .rat(Position(0, 0)) \
    .finish(Position(7, 5)) \
    .add_cheese(Position(0, 5)) \
    .add_cheese(Position(3, 1)) \
    .add_cheese(Position(6, 3)) \
    .add_wall(Position(1, 2)) \
    .add_wall(Position(6, 2)) \
    .add_trap(Position(5, 0)) \
    .add_trap(Position(2, 4)) \
    .add_hole(Position(1, 0)) \
    .add_hole(Position(4, 3)) \
    .build() \
    .save(6)

# level seven
Level.builder(id=7, width=10, height=8) \
    .rat(Position(0, 0)) \
    .finish(Position(9, 7)) \
    .add_cheese(Position(0, 7)) \
    .add_cheese(Position(4, 1)) \
    .add_cheese(Position(7, 3)) \
    .add_wall(Position(2, 2)) \
    .add_wall(Position(7, 2)) \
    .add_trap(Position(6, 0)) \
    .add_trap(Position(3, 6)) \
    .add_hole(Position(1, 1)) \
    .add_hole(Position(5, 5)) \
    .build() \
    .save(7)

# level eight
Level.builder(id=8, width=12, height=10) \
    .rat(Position(0, 0)) \
    .finish(Position(11, 9)) \
    .add_cheese(Position(0, 9)) \
    .add_cheese(Position(5, 1)) \
    .add_cheese(Position(9, 3)) \
    .add_wall(Position(3, 2)) \
    .add_wall(Position(8, 2)) \
    .add_trap(Position(7, 0)) \
    .add_trap(Position(4, 7)) \
    .add_hole(Position(1, 1)) \
    .add_hole(Position(6, 6)) \
    .build() \
    .save(8)

# level nine
Level.builder(id=9, width=7, height=5) \
    .rat(Position(0, 0)) \
    .finish(Position(6, 4)) \
    .add_cheese(Position(0, 4)) \
    .add_cheese(Position(3, 1)) \
    .add_wall(Position(1, 2)) \
    .add_trap(Position(4, 0)) \
    .add_hole(Position(1, 0)) \
    .build() \
    .save(9)

# level ten
Level.builder(id=10, width=9, height=7) \
    .rat(Position(0, 0)) \
    .finish(Position(8, 6)) \
    .add_cheese(Position(0, 6)) \
    .add_cheese(Position(3, 1)) \
    .add_cheese(Position(6, 3)) \
    .add_wall(Position(1, 2)) \
    .add_wall(Position(7, 2)) \
    .add_trap(Position(5, 0)) \
    .add_trap(Position(2, 5)) \
    .add_hole(Position(1, 0)) \
    .add_hole(Position(4, 4)) \
    .build() \
    .save(10)
