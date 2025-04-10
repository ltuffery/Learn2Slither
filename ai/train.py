from engine.game import Game
from engine.direction import Direction
import numpy as np
import csv
import engine.settings as settings
from engine.exception.gameover import GameOver

# Exploration rate
EPSILON = settings.EPSILON

# Q-table: maps (state, action) pairs to Q-values
Q = {}


def progress_bar(i: int) -> None:
    """
    Displays a progress bar in the console during training.

    Args:
        i (int): The current episode number.
    """
    progress_blocks = 20
    progress_ratio = i / settings.EPISODES
    filled_blocks = int(progress_ratio * progress_blocks)

    load_bar = "#" * filled_blocks + " " * (progress_blocks - filled_blocks)
    print(f"\r[{load_bar}] {i}/{settings.EPISODES}", end="")

    if i == settings.EPISODES:
        print("")


def get_Q(state: list[bool], action: int) -> float:
    """
    Retrieves the Q-value for a given (state, action) pair.

    Args:
        state (list[bool]): The current state of the agent (snake).
        action (int): The action index (0 to 3, representing directions).

    Returns:
        float: The Q-value for the given pair, or 0.0 if not yet defined.
    """
    return Q.get((tuple(state), action), 0.0)


def action(state: list[bool]) -> int:
    """
    Selects an action using the epsilon-greedy policy.

    Args:
        state (list[bool]): The current state.

    Returns:
        int: The index of the selected action.
    """
    global EPSILON

    if np.random.uniform() < EPSILON:
        return np.random.randint(0, len(Direction))  # Exploration
    else:
        return max(range(4), key=lambda a: get_Q(state, a))  # Exploitation


def train() -> None:
    """
    Trains the snake agent using Q-learning.

    - Initializes a new game environment for each episode.
    - Updates the Q-table based on the rewards received.
    - Saves rewards and the Q-table to CSV files after training.
    """
    global EPSILON

    env = Game()
    env.start()
    snake = env.get_snake()
    all_action: list[list] = list()

    # Create rewards log file
    with open("data/rewards.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Total_Reward"])

        for i in range(settings.EPISODES):
            isLast = False
            env.start()
            snake = env.get_snake()
            s = snake.get_state()
            total_reward = 0
            all_action.append(list())

            while not isLast:
                a = action(s)
                try:
                    r = snake.move(list(Direction)[a])
                except GameOver:
                    isLast = True
                    r = settings.GAMEOVER_REWARD  # Penalty for dying

                s_next = snake.get_state()

                # Q-learning update rule
                next_action = max(range(4), key=lambda a: get_Q(s_next, a))
                next_q = get_Q(s_next, next_action)
                Q[(tuple(s), a)] = get_Q(s, a) + settings.ALPHA * (
                    r + settings.GAMMA * next_q - get_Q(s, a)
                )

                total_reward += r
                s = s_next
                all_action[i].append(tuple(s))

            progress_bar(i + 1)

            writer.writerow([total_reward])

            EPSILON *= settings.EPSILON_DECAY
            EPSILON = max(EPSILON, settings.EPSILON_MIN)

        # Save Q-table to CSV
        with open("data/q_table.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["State", "Action", "Q_Value"])

            for (state, a), q_value in Q.items():
                writer.writerow([state, list(Direction)[a].name, q_value])


# Start training when this script is run
train()
