from engine.game import Game
from engine.direction import Direction
import engine.settings as settings
from engine.exception.gameover import GameOver
from ai.utils import QNetwork
import torch
import torch.optim as optim
import random


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


# Hyperparamètres
BATCH_SIZE = 32
TARGET_UPDATE_FREQUENCY = 10
LEARNING_RATE = 1e-3


def train_dqn(model, target_model, replay_buffer, optimizer):
    if len(replay_buffer) < BATCH_SIZE:
        return

    transitions = replay_buffer.sample(BATCH_SIZE)
    batch = list(zip(*transitions))

    states = torch.tensor(batch[0], dtype=torch.float32)
    actions = torch.tensor(batch[1], dtype=torch.long)
    rewards = torch.tensor(batch[2], dtype=torch.float32)
    next_states = torch.tensor(batch[3], dtype=torch.float32)
    dones = torch.tensor(batch[4], dtype=torch.uint8)

    current_q_values = model(states).gather(1, actions.unsqueeze(1)).squeeze(1)

    next_q_values = target_model(next_states).max(1)[0]
    target_q_values = rewards + (settings.GAMMA * next_q_values * (1 - dones))

    loss = torch.mean((current_q_values - target_q_values) ** 2)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# Exploration rate
EPSILON = settings.EPSILON


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
    global EPSILON

    env = Game()
    all_action = []

    input_size = len(env.get_snake().get_state())
    output_size = len(Direction)
    model = QNetwork(input_size, output_size)
    target_model = QNetwork(input_size, output_size)
    target_model.load_state_dict(model.state_dict())
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    replay_buffer = ReplayBuffer(capacity=10000)

    for i in range(settings.EPISODES):
        is_last = False
        env.start()
        snake = env.get_snake()
        s = snake.get_state()
        all_action.append([])

        while not is_last:
            if random.random() < EPSILON:
                a = random.randint(0, 3)  # Exploration
            else:
                q_values = model(torch.tensor(s, dtype=torch.float32))
                a = torch.argmax(q_values).item()  # Exploitation

            try:
                r = snake.move(list(Direction)[a])
            except GameOver:
                is_last = True
                r = settings.GAMEOVER_REWARD

            s_next = snake.get_state()
            done = is_last

            replay_buffer.push(s, a, r, s_next, done)

            train_dqn(model, target_model, replay_buffer, optimizer)

            s = s_next

        if i % TARGET_UPDATE_FREQUENCY == 0:
            target_model.load_state_dict(model.state_dict())

        EPSILON *= settings.EPSILON_DECAY
        EPSILON = max(EPSILON, settings.EPSILON_MIN)

        progress_bar(i + 1)

    torch.save(model.state_dict(), "dqn_model.pth")

    print("Entraînement terminé !")


if __name__ == "__main__":
    train("train")
