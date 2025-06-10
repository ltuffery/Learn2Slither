from engine.game import Game
from engine.direction import Direction
import csv
import engine.settings as settings
from engine.exception.gameover import GameOver
import ai.replay as replay
from ai.utils import get_Q, action

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


def train(filename: str) -> None:
    """
    Trains the snake agent using Q-learning.

    - Initializes a new game environment for each episode.
    - Updates the Q-table based on the rewards received.
    - Saves rewards and the Q-table to CSV files after training.
    """
    global EPSILON

    env = Game()
    all_action: list[list] = list()

    # Create rewards log file
    with open(f"data/{filename}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Total_Reward"])

        for i in range(settings.EPISODES):
            isLast = False
            env.start()
            snake = env.get_snake()
            s = snake.get_state()
            total_reward = 0
            all_action.append(list())
            replay.reset_replay()

            while not isLast:
                a = action(Q, s, EPSILON)
                try:
                    r = snake.move(list(Direction)[a])
                except GameOver:
                    isLast = True
                    r = settings.GAMEOVER_REWARD  # Penalty for dying

                replay.save_game_state(env, list(Direction)[a])
                s_next = snake.get_state()

                # Q-learning update rule
                next_action = max(range(4), key=lambda a: get_Q(Q, s_next, a))
                next_q = get_Q(Q, s_next, next_action)
                Q[(tuple(s), a)] = get_Q(Q, s, a) + settings.ALPHA * (
                    r + settings.GAMMA * next_q - get_Q(Q, s, a)
                )

                if r > 0:
                    total_reward += 1
                s = s_next
                all_action[i].append(tuple(s))

            progress_bar(i + 1)

            writer.writerow([total_reward])

            EPSILON *= settings.EPSILON_DECAY
            EPSILON = max(EPSILON, settings.EPSILON_MIN)

        replay.create_replay()
        # Save Q-table to CSV
        with open("data/q_table.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["State", "Action", "Q_Value"])

            for (state, a), q_value in Q.items():
                writer.writerow([state, list(Direction)[a].name, q_value])

if __name__ == "__main__":
    train("rewards")
