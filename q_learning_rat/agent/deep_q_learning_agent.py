from turtle import st
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from q_learning_rat.agent.q_table_agent import QTableAgent
from q_learning_rat.model.position import Position


class DeepQNetwork(nn.Module):
    def __init__(self, view_distance: int = 0):
        super().__init__()
        self.view_distance = view_distance
        self.layers = nn.Sequential(
            nn.Linear((2 * view_distance + 1) ** 2 +1, 100),
            nn.ReLU(),
            nn.Linear(100, 4)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if len(x.shape) == 1:
            x = x.unsqueeze(0)

        return self.layers(x)
    
    def clone(self) -> "DeepQNetwork":
        model = DeepQNetwork(self.view_distance)
        model.load_state_dict(self.state_dict())
        return model
    
class DeepQLearningAgent(QTableAgent):
    def __init__(
            self, 
            view_distance: int = 3, 
            learning_rate: float = 1e-3, 
            discount_factor: float = 1,
            position_penalty_start: float = -0.001, 
            position_penalty_end: float = -0.5,
            position_penalty_decay: float = 5
        ):
        super().__init__(
            discount_factor=discount_factor,
            learning_rate=learning_rate,
            position_penalty_start=position_penalty_start,
            position_penalty_end=position_penalty_end,
            position_penalty_decay=position_penalty_decay
        )
        self.view_distance = view_distance
        self.prev_model = DeepQNetwork(view_distance)
        self.model = self.prev_model.clone()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()

    def policy(self, state: np.ndarray) -> int:
        state = self.state(state)
        return np.argmax(self.model.forward(torch.tensor(state, dtype=torch.float32)).detach().numpy())

    def state(self, state: np.ndarray) -> np.ndarray:
        state = state[2:].copy()
        k = 0
        for i in range(-self.view_distance, self.view_distance+1):
            for j in range(-self.view_distance, self.view_distance+1):
                if i == 0 and j == 0:
                    continue
                if state[k] == 0:
                    state[k] = -1
                elif state[k] == 1:
                    state[k] = self.reward("cheese")
                elif state[k] == 2:
                    state[k] = self.reward("dead")
                elif state[k] == 3:
                    state[k] = self.reward("finish")
                elif state[k] == 4:
                    state[k] = self._get_position_penalty(Position(i, j), increase=False)
                else:
                    raise ValueError(f"Invalid state: {state[k]}")
                k += 1
        return state

    def name(self) -> str:
        return "Deep Q-Learning Agent"

    def reset(self):
        self.model = DeepQNetwork(self.view_distance)
        self.prev_model = self.model.clone()
    
    def interaction(self, initial_state: np.ndarray, result_state: np.ndarray, action: int, interaction: str, terminated: bool = False):
        reward = self.reward(interaction)
        initial_state = self.state(initial_state)
        result_state = self.state(result_state)
        
        prev_model = self.model.clone()
        actual_reward = self.model.forward(torch.tensor(initial_state, dtype=torch.float32))[0, action]
        expected_reward = reward + self.discount_factor * self.prev_model.forward(torch.tensor(result_state, dtype=torch.float32)).max()
        loss = self.criterion(actual_reward, expected_reward)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.prev_model = prev_model
