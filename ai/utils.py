import numpy as np
from engine.direction import Direction
import torch
import torch.nn as nn


def get_Q(Q: dict, state: list[bool], action: int) -> float:
    """
    Retrieves the Q-value for a given (state, action) pair.

    Args:
        Q (dict): The Q-table mapping (state, action) pairs to Q-values.
        state (list[bool]): The current state of the agent (snake).
        action (int): The action index (0 to 3, representing directions).

    Returns:
        float: The Q-value for the given pair, or 10.0 if not yet defined.
    """
    return Q.get((tuple(state), action), 10.0)


def action(Q, state, epsilon):
    # L'epsilon-greedy n'est plus nécessaire puisque l'on fait déjà de l'exploitation avec DQN.
    return torch.argmax(Q(state)).item()


class QNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
