from code import InteractiveConsole
import random
from typing import List

import numpy as np
import pygame
from q_learning_rat.agent.abstract_agent import AbstractAgent
from q_learning_rat.input import Input
from q_learning_rat.model.level import Level
from q_learning_rat.model.move import Move
from q_learning_rat.view.level_renderer import LevelView


class BasicTrainer:
    def __init__(
            self, 
            level_ids: List[int],
            agents: List[AbstractAgent],
            epsilon_start: float = 0.5, 
            epsilon_end: float = 0.01, 
            epsilon_decay: float = 0.9, 
            view_distance: int = 0,
        ):
        self.level_ids = level_ids
        self.level_id_idx = 0
        self.level = Level.load(self.level_id)
        self.agents = agents
        self.agent_idx = 0
        self.agent.start(self.level)
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.epsilon = epsilon_start
        self.view_distance = view_distance

    @property
    def level_id(self):
        return self.level_ids[self.level_id_idx]
    
    @property
    def agent(self):
        return self.agents[self.agent_idx]

    def restart(self):
        if not self.level.dead:
            self.epsilon = max(self.epsilon*self.epsilon_decay, self.epsilon_end)
            # print(f'Epsilon: {self.epsilon}')
        self.last_score = self.level.score
        self.level = self.level.load(self.level_id)
        self.agent.start(self.level)

    def _reset_agent_and_level(self):
        self.agent.reset()
        self.epsilon = self.epsilon_start
        self.restart()

    def _next_level(self):
        self.level_id_idx = (self.level_id_idx+1)%len(self.level_ids)
        self.restart()

    def _prev_level(self):
        self.level_id_idx = (self.level_id_idx-1+len(self.level_ids))%len(self.level_ids)
        self.restart()

    def _next_agent(self):
        self.agent_idx = (self.agent_idx+1)%len(self.agents)
        self._reset_agent_and_level()

    def _prev_agent(self):
        self.agent_idx = (self.agent_idx-1+len(self.agents))%len(self.agents)
        self._reset_agent_and_level()

    def step(self) -> Level:
        if Input.key_pressed(pygame.K_RIGHT):
            self._next_level()
        if Input.key_pressed(pygame.K_LEFT):
            self._prev_level()
        if Input.key_pressed(pygame.K_UP):
            self._next_agent()
        if Input.key_pressed(pygame.K_DOWN):
            self._prev_agent()
        if Input.key_pressed(pygame.K_r):
            self._reset_agent_and_level()

        initial_state = self.level.state(self.view_distance)
        action = self.agent.policy(initial_state)
        if action is not None:
            if random.random() < self.epsilon:
                action = random.randint(0, 3)

            interaction = self.level.move(Move.from_action(action))
            self.agent.interaction(initial_state, self.level.state(self.view_distance), action, interaction, terminated=self.level.done)
            
            if self.level.done:
                self.restart()
        return self.level
