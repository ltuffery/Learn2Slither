from engine.game import Game
from engine.direction import Direction
import csv
import engine.settings as settings
from engine.exception.gameover import GameOver
import ai.replay as replay
from ai.utils import QNetwork
import torch
import torch.optim as optim
import random
import numpy as np


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

    # Échantillonnage du mini-lot
    transitions = replay_buffer.sample(BATCH_SIZE)
    batch = list(zip(*transitions))

    states = torch.tensor(batch[0], dtype=torch.float32)
    actions = torch.tensor(batch[1], dtype=torch.long)
    rewards = torch.tensor(batch[2], dtype=torch.float32)
    next_states = torch.tensor(batch[3], dtype=torch.float32)
    dones = torch.tensor(batch[4], dtype=torch.uint8)

    # Q-values prédites par le modèle
    current_q_values = model(states).gather(1, actions.unsqueeze(1)).squeeze(1)

    # Q-values cibles
    next_q_values = target_model(next_states).max(1)[0]
    target_q_values = rewards + (settings.GAMMA * next_q_values * (1 - dones))

    # Calcul de la perte
    loss = torch.mean((current_q_values - target_q_values) ** 2)

    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

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
    global EPSILON

    # Initialisation de l'environnement et du réseau
    env = Game()
    all_action = []

    # Initialisation du modèle et du target network
    input_size = len(env.get_snake().get_state())  # La taille de l'état
    output_size = 4  # Nombre d'actions possibles (haut, bas, gauche, droite)
    model = QNetwork(input_size, output_size)
    target_model = QNetwork(input_size, output_size)
    target_model.load_state_dict(model.state_dict())  # Copier les poids du modèle initial
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # Replay buffer
    replay_buffer = ReplayBuffer(capacity=10000)

    # Fichier CSV pour enregistrer les résultats
    with open(f"data/{filename}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["State", "Action", "Q_Value"])

        for i in range(settings.EPISODES):
            is_last = False
            env.start()
            snake = env.get_snake()
            s = snake.get_state()
            all_action.append([])

            while not is_last:
                # Choisir l'action avec epsilon-greedy
                if random.random() < EPSILON:
                    a = random.randint(0, 3)  # Exploration
                else:
                    q_values = model(torch.tensor(s, dtype=torch.float32))
                    a = torch.argmax(q_values).item()  # Exploitation

                try:
                    r = snake.move(list(Direction)[a])
                except GameOver:
                    is_last = True
                    r = settings.GAMEOVER_REWARD  # Pénalité pour la fin du jeu

                s_next = snake.get_state()
                done = is_last

                # Enregistrer dans le Replay Buffer
                replay_buffer.push(s, a, r, s_next, done)

                # Entraînement DQN
                train_dqn(model, target_model, replay_buffer, optimizer)

                # Mise à jour de l'état
                s = s_next

            # Mise à jour du target network à intervalles réguliers
            if i % TARGET_UPDATE_FREQUENCY == 0:
                target_model.load_state_dict(model.state_dict())

            # Sauvegarde des résultats
            writer.writerow([snake.get_size()])

            # Mise à jour de l'EPSILON pour favoriser l'exploitation
            EPSILON *= settings.EPSILON_DECAY
            EPSILON = max(EPSILON, settings.EPSILON_MIN)

            progress_bar(i + 1)

        # Sauvegarder le modèle
        torch.save(model.state_dict(), "dqn_model.pth")

        print("Entraînement terminé !")

if __name__ == "__main__":
    train("train")
