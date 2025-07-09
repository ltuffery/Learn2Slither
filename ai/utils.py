import numpy as np
from engine.direction import Direction


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


def action(Q: dict, state: list[bool], explo: float) -> int:
    """
    Chooses an action using the epsilon-greedy strategy.

    This function selects an action based on the current state:
    - With a probability of `explo` (exploration rate), it chooses a random
    action.
    - Otherwise, it chooses the action that maximizes the Q-value for the
    given state (exploitation).

    Args:
        Q (dict): The Q-table mapping (state, action) pairs to Q-values.
        state (list[bool]): The current perception/state of the agent
        (e.g., snake vision).
        explo (float): The exploration rate (epsilon), between 0 and 1.

    Returns:
        int: The index of the selected action
        (e.g., 0 to 3 corresponding to directions).
    """
    if np.random.uniform() < explo:
        return np.random.randint(0, len(Direction))  # Exploration
    else:
        return max(range(4), key=lambda a: get_Q(Q, state, a))  # Exploitation
