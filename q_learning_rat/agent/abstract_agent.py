from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from q_learning_rat.model.level import Level


class AbstractAgent(ABC):
    @abstractmethod
    def policy(self, state: np.ndarray) -> Optional[int]:
        pass

    @abstractmethod
    def interaction(self, initial_state: np.ndarray, result_state: np.ndarray, action: int, interaction: str, terminated: bool = False):
        pass

    @abstractmethod
    def start(self, level: Level):
        pass