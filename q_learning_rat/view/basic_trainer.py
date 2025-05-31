from code import InteractiveConsole
import random

import numpy as np
from q_learning_rat.agent.abstract_agent import AbstractAgent
from q_learning_rat.model.level import Level
from q_learning_rat.model.move import Move
from q_learning_rat.view.abstract_trainer import AbstractTrainer
from q_learning_rat.view.level_renderer import LevelView


class BasicTrainer(AbstractTrainer):
    def __init__(
            self, 
            level_id: int, 
            agent: AbstractAgent, 
            epsilon_start: float = 0.5, 
            epsilon_end: float = 0.01, 
            epsilon_decay: float = 0.9, 
            view_distance: int = 0,
        ):
        self.level_id = level_id
        self.level = Level.load(self.level_id)
        self.agent = agent
        self.agent.start(self.level)
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.epsilon = epsilon_start
        self.view_distance = view_distance

    def restart(self):
        if not self.level.dead:
            self.epsilon = max(self.epsilon*self.epsilon_decay, self.epsilon_end)
            # print(f'Epsilon: {self.epsilon}')
        self.last_score = self.level.score
        self.level = self.level.restart()
        self.agent.start(self.level)

    def step(self) -> Level:
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