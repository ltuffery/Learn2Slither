import torch
import torch.optim as optim
import torch.multiprocessing as mp
from collections import deque
import random
import time

from engine.game import Game
from engine.direction import Direction
import engine.settings as settings
from engine.exception.gameover import GameOver
from ai.utils import QNetwork


BATCH_SIZE = 32
TARGET_UPDATE_FREQUENCY = 10
LEARNING_RATE = 1e-3
NUM_PROCESSES = 12  # nombre de processus à utiliser


class SharedReplayBuffer:
    def __init__(self, capacity, lock):
        self.buffer = deque(maxlen=capacity)
        self.lock = lock

    def push(self, state, action, reward, next_state, done):
        with self.lock:
            self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        with self.lock:
            return random.sample(self.buffer, batch_size)

    def __len__(self):
        with self.lock:
            return len(self.buffer)


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


def progress_bar(i: int) -> None:
    progress_blocks = 20
    progress_ratio = i / settings.EPISODES
    filled_blocks = int(progress_ratio * progress_blocks)

    load_bar = "#" * filled_blocks + " " * (progress_blocks - filled_blocks)
    print(f"\r[{load_bar}] {i}/{settings.EPISODES}", end="")

    if i == settings.EPISODES:
        print("")


def worker(process_id, model, target_model, replay_buffer, lock):
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    EPSILON = settings.EPSILON

    env = Game()
    input_size = len(env.get_snake().get_state())

    for i in range(settings.EPISODES // NUM_PROCESSES):
        is_last = False
        env.start()
        snake = env.get_snake()
        s = snake.get_state()

        while not is_last:
            if random.random() < EPSILON:
                a = random.randint(0, 3)
            else:
                with torch.no_grad():
                    q_values = model(torch.tensor(s, dtype=torch.float32))
                    a = torch.argmax(q_values).item()

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

        if process_id == 0:
            progress_bar(i + 1)


if __name__ == "__main__":
    mp.set_start_method("spawn")  # 'spawn' est recommandé pour compatibilité

    env = Game()
    input_size = len(env.get_snake().get_state())
    output_size = len(Direction)

    model = QNetwork(input_size, output_size)
    model.share_memory()

    target_model = QNetwork(input_size, output_size)
    target_model.load_state_dict(model.state_dict())
    target_model.share_memory()

    manager = mp.Manager()
    lock = manager.Lock()
    replay_buffer = SharedReplayBuffer(capacity=10000, lock=lock)

    processes = []
    for pid in range(NUM_PROCESSES):
        p = mp.Process(target=worker, args=(pid, model, target_model, replay_buffer, lock))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    torch.save(model.state_dict(), "dqn_model.pth")
    print("\nEntraînement multiprocess terminé.")
