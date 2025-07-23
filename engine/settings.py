# Rewards
# RED_APPLE_PENALTY = -25  # Increased penalty for eating a red apple
# GREEN_APPLE_BONUS = 200  # Increased bonus for eating a green apple
# GAMEOVER_REWARD = -500   # Increased penalty for game over
# EAT_NOTHING_REWARD = -1  # Small penalty for each step without eating
# TIME_ALIVE_REWARD = 0.1  # Small positive reward for each step the snake stays alive
# SIZE_REWARD_MULTIPLIER = 0.5  # Reward proportional to current snake size (per step)
# TARGET_LENGTH = 30       # Target snake length for an additional large bonus
# TARGET_LENGTH_BONUS = 500  # Large bonus for reaching the target length
# SIZE_MILESTONE_BONUS = 50  # Bonus for hitting size milestones (e.g., every 5 segments)

GREEN_APPLE_BONUS = 50.0   # Forte récompense pour manger une pomme verte
RED_APPLE_PENALTY = -25.0  # Pénalité modérée pour manger une pomme rouge
EAT_NOTHING_REWARD = -0.1  # Légère pénalité à chaque pas sans manger
TIME_ALIVE_REWARD = 0.1    # Petite récompense pour chaque pas en vie
SIZE_REWARD_MULTIPLIER = 0.5 # Récompense proportionnelle à la taille
GAMEOVER_REWARD = -200.0   # Très forte pénalité pour perdre

TARGET_LENGTH = 30
TARGET_LENGTH_BONUS = 100.0 # Bonus si la taille atteint la cible
SIZE_MILESTONE_BONUS = 20.0 # Bonus pour chaque "palier" de taille (ex: tous les 5 segments)

# Display Characters
RED_APPLE_CHAR = "~"       # Character for red apple
GREEN_APPLE_CHAR = "@"     # Character for green apple
WALL_CHAR = "*"            # Character for walls
SNAKE_HEAD_CHAR = "#"      # Character for snake's head
SNAKE_SEGMENT_CHAR = "o"   # Character for snake's body segments
EMPTY_CHAR = " "           # Character for empty cells on the map

# AI Training Hyperparameters
EPISODES = 2000         # Number of episodes for training
ALPHA = 0.1              # Learning rate (alpha)
GAMMA = 0.99             # Discount factor (gamma)
EPSILON = 1.0            # Initial exploration rate (1.0 = 100% exploration)
EPSILON_DECAY = 0.995    # Decay rate for epsilon (e.g., 0.995 for slower decay)
EPSILON_MIN = 0.01       # Minimum exploration rate

# World Dimensions
HEIGHT = 10              # Height of the playable area of the world
WIDTH = 10               # Width of the playable area of the world

# Game specific settings
INITIAL_SNAKE_LENGTH = 3 # Initial length of the snake (head + body segments)