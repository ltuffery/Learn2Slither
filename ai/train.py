from engine.game import Game
from api.direction import Direction
import numpy as np
import csv
from engine.exception.gameover import GameOver


GRID_SIZE = 10
EPISODES = 5000
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 1.0
EPSILON_DECAY = 0.995

Q = {}

def get_Q(state, action):
    return Q.get((tuple(state), action), 0.0)

def action(state):
    global EPSILON

    if np.random.uniform() < EPSILON:
        return np.random.randint(0, len(Direction)) # Exploration
    else:
        return max(range(4), key=lambda a: get_Q(state, a)) # Exploitation

def train():
    global EPSILON

    env = Game()
    env.start()
    snake = env.get_snake()
    all_action:list[list] = list()

    with open("data/rewards.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Total_Reward"])  # En-tête du fichier CSV

        for i in range(EPISODES):
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
                    r = -15
                
                s_next = snake.get_state()

                best_next_action = max(range(4), key=lambda a: get_Q(s_next, a))
                Q[(tuple(s), a)] = get_Q(s, a) + ALPHA * (
                    r + GAMMA * get_Q(s_next, best_next_action) - get_Q(s, a)
                )

                total_reward += r
                s = s_next

                all_action[i].append(tuple(s))

            print(f"Épisode {i}, Score: {total_reward}")
            writer.writerow([total_reward])
        
            EPSILON *= EPSILON_DECAY
            EPSILON = max(EPSILON, 0.01)  # Ne descend pas sous 1%
        
        with open("data/q_table.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["State", "Action", "Q_Value"])  # En-tête du fichier CSV

            for (state, a), q_value in Q.items():
                writer.writerow([state, list(Direction)[a].name, q_value])

train()