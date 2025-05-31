import pickle
import random
import re
from typing import Tuple
import numpy as np

from q_learning_rat.agent.abstract_agent import AbstractAgent
from q_learning_rat.model.level import Level
from q_learning_rat.model.position import Position


class QTableAgent(AbstractAgent):
    def __init__(
            self, 
            discount_factor: float = 1, 
            learning_rate: float = 1e-3, 
            q_table: dict = None, 
            position_penalty_start: float = -0.005, 
            position_penalty_end: float = -0.5,
            position_penalty_decay: float = 2
        ):
        self.q_table = q_table or {}
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.level = None
        self.position_penalty = None
        self.position_penalty_start = position_penalty_start
        self.position_penalty_end = position_penalty_end
        self.position_penalty_decay = position_penalty_decay

    def __get_q_value(self, state: np.ndarray, action: int) -> float:
        state = self.__to_index(state)
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = random.random()
        return self.q_table[state][action]
    
    def __set_q_value(self, state: np.ndarray, action: int, value: float):  
        state = self.__to_index(state)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = value

    def __to_index(self, state: np.ndarray) -> Tuple[int, int]:
        return int(state[0]), int(state[1])

    def policy(self, state: np.ndarray) -> int:
        state = self.state(state)
        return np.argmax(np.array([self.__get_q_value(state, action) for action in range(4)]))

    def _get_position_penalty(self, position: Position, increase: bool = False) -> float:
        if position not in self.position_penalty:
            self.position_penalty[position] = self.position_penalty_start
        penalty = self.position_penalty[position]
        if increase:
            self.position_penalty[position] = min(self.position_penalty[position] * self.position_penalty_decay, self.position_penalty_end)
        return penalty
    
    def reward(self, interaction: str) -> float:
        if interaction == "cheese":
            return 0.5
        elif interaction == "finish":
            return 0.2
        elif interaction == "dead":
            return -1
        elif interaction == "move" or interaction == "none":
            return self._get_position_penalty(self.level.rat, increase=True)
        else:
            raise ValueError(f"Invalid interaction: {interaction}")
        
    def state(self, state: np.ndarray) -> np.ndarray:
        return state[:2]
        
    def start(self, level: Level):
        self.level = level
        self.position_penalty = {}
    
    def interaction(self, initial_state: np.ndarray, result_state: np.ndarray, action: int, interaction: str, terminated: bool = False):
        reward = self.reward(interaction)
        initial_state = self.state(initial_state)
        result_state = self.state(result_state)

        if terminated:
            self.__set_q_value(result_state, action, reward)

        expected_reward = reward + self.discount_factor * self.__get_q_value(result_state, self.policy(result_state))
        actual_reward = self.__get_q_value(initial_state, action)
        self.__set_q_value(
            initial_state, 
            action, 
            actual_reward - self.learning_rate * (actual_reward - expected_reward)
        )

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'rb') as f:
            q_table = pickle.load(f)
        agent = cls(level=None, q_table=q_table)
        return agent