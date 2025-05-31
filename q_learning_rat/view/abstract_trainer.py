from abc import ABC, abstractmethod
from q_learning_rat.model.level import Level


class AbstractTrainer(ABC):
    @abstractmethod
    def step(self) -> Level:
        pass