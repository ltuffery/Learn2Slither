#  Rewards
RED_APPLE_REWARD = -15
GREEN_APPLE_REWARD = 10
GAMEOVER_REWARD = -1

#  Display
RED_APPLE_CHAR = "~"
GREEN_APPLE_CHAR = "."
WALL_CHAR = "*"
SNAKE_HEAD_CHAR = "#"
SNAKE_SEGMENT_CHAR = "o"

# AI Train
EPISODES = 5000
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 1.0  # 1.0 == 100%
EPSILON_DECAY = 0.995 #  Set 1.0 for an EPSILON strategy
EPSILON_MIN = 0.01
