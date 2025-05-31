from typing import Optional
import pygame
from q_learning_rat.agent.abstract_agent import AbstractAgent

import numpy as np

from q_learning_rat.input import Input
from q_learning_rat.model.level import Level
from q_learning_rat.model.move import Move


class InputAgent(AbstractAgent):
    def policy(self, state: np.ndarray) -> Optional[int]:
        if Input.key_pressed(pygame.K_LEFT):
            return Move.left().action
        elif Input.key_pressed(pygame.K_RIGHT):
            return Move.right().action
        elif Input.key_pressed(pygame.K_UP):
            return Move.up().action
        elif Input.key_pressed(pygame.K_DOWN):
            return Move.down().action
        else:
            return None

    def interaction(self, initial_state: np.ndarray, result_state: np.ndarray, action: int, interaction: str, terminated: bool = False):
        pass

    def start(self, level: Level):
        pass

    def name(self) -> str:
        return "Input Agent"

    def reset(self):
        pass
