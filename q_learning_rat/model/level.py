from dataclasses import dataclass
from hmac import new
import pickle
import random
from turtle import done
from typing import Set

import numpy as np

from q_learning_rat.model.move import Move
from q_learning_rat.model.position import Position


@dataclass
class Level:
    __FINISH_SCORE = 100
    __CHEESE_SCORE = 20
    __FEAR_EPSILON = 0.1
    __DEATH_TIME = 300

    id: int
    width: int
    height: int
    rat: Position
    cheeses: Set[Position]
    holes: Set[Position]
    traps: Set[Position]
    walls: Set[Position]
    finish: Position
    time: int
    score: int
    dead: bool # true if rat is dead
    done: bool # true if at finish or dead

    def __post_init__(self):
        self.fear_positions = {}
        for position in self.traps:
            for action in range(4):
                fear_position = position.translate(Move.from_action(action))
                self.fear_positions[fear_position] = position

    def contains(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height
    
    def state(self, view_distance: int = 0) -> np.ndarray:
        positions = []

        for i in range(-view_distance, view_distance+1):
            for j in range(-view_distance, view_distance+1):
                if i == 0 and j == 0:
                    continue
                position = self.rat.translate(Move(i, j, -1))
                if not self.contains(position) or position in self.walls:
                    positions.append(0)
                elif position in self.cheeses:
                    positions.append(1)
                elif position in self.holes or position in self.traps:
                    positions.append(2)
                elif position == self.finish:
                    positions.append(3)
                else:
                    positions.append(4)

        return np.array([self.rat.x, self.rat.y, *positions, abs(self.rat.x - self.finish.x)/self.width, abs(self.rat.y - self.finish.y)/self.height])
    
    def move(self, move: Move) -> str:
        new_position = self.rat.translate(move)
        if self.rat in self.fear_positions:
            if random.random() < self.__FEAR_EPSILON:
                new_position = self.fear_positions[self.rat]

        self.time += 1

        if not self.contains(new_position) or new_position in self.walls:
            return "none"

        self.rat = new_position

        if self.time > self.__DEATH_TIME:
            self.dead = True
            self.done = True
            return "dead"

        elif self.rat in self.holes or self.rat in self.traps:
            self.dead = True
            self.done = True
            return "dead"
        
        elif self.rat in self.cheeses:
            self.cheeses.remove(self.rat)
            self.score += self.__CHEESE_SCORE
            return "cheese"

        elif self.rat == self.finish:
            self.done = True
            self.score += self.__FINISH_SCORE
            return "finish"
        
        return "move"
    

    def save(self, level: int):
        with open(f"levels/level_{level}.pkl", "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, level: int) -> "Level":
        with open(f"levels/level_{level}.pkl", "rb") as f:
            return pickle.load(f)
        
    def restart(self) -> "Level":
        return Level.load(self.id)
        
    @classmethod
    def builder(cls, id: int, width: int, height: int) -> "LevelBuilder":
        return LevelBuilder(id, width, height)
        
class LevelBuilder:
    def __init__(self, id: int, width: int, height: int):
        self.id = id
        self.width = width
        self.height = height
        self.cheeses = set()
        self.holes = set()
        self.traps = set()
        self.walls = set()
        self.__finish = None
        self.__rat = None

    def add_cheese(self, position: Position) -> "LevelBuilder":
        self.cheeses.add(position)
        return self
    
    def add_hole(self, position: Position) -> "LevelBuilder":
        self.holes.add(position)
        return self
    
    def add_trap(self, position: Position) -> "LevelBuilder":
        self.traps.add(position)
        return self
    
    def add_wall(self, position: Position) -> "LevelBuilder":
        self.walls.add(position)
        return self
    
    def finish(self, position: Position) -> "LevelBuilder":
        self.__finish = position
        return self
    
    def rat(self, position: Position) -> "LevelBuilder":
        self.__rat = position
        return self
    
    def build(self) -> "Level":
        assert self.__rat is not None
        assert self.__finish is not None

        return Level(
            id=self.id,
            width=self.width,
            height=self.height,
            cheeses=self.cheeses,
            holes=self.holes,
            traps=self.traps,
            walls=self.walls,
            finish=self.__finish,
            rat=self.__rat,
            time=0,
            score=0,
            dead=False,
            done=False,
        )