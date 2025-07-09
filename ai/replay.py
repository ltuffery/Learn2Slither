from engine.game import Game
from engine.entity.apple import Apple
from engine.entity.snake import Snake
from engine.direction import Direction
import json
import time
import sys
import os

# Global storage for recorded gameplay
replay_storage = []
replay_data = []


def reset_replay():
    """
    Saves the current replay data to the replay storage and resets the current
    replay buffer.

    This is typically called at the end of a game episode to archive the
    episode's data.
    """
    global replay_data
    global replay_storage

    if len(replay_data) > 0:
        replay_storage.append(replay_data)
    replay_data = []


def save_game_state(game: Game, direction: Direction):
    """
    Save the current game state along with the snake's direction.

    Captures the snake's head position, body, and all apples on the map,
    including their color, and appends this data to the global replay log.

    Args:
        game (Game): The current game instance to record.
        direction (Direction): The current direction of the snake.
    """
    global replay_data

    data = {
        "direction": direction.name,
        "apples": [],
    }

    for entity in game.get_world().get_entities():
        if isinstance(entity, Apple):
            apple = (entity.get_x(), entity.get_y(), entity.is_green())

            data["apples"].append(apple)
        elif isinstance(entity, Snake):
            data["head"] = entity.get_position()
            data["body"] = list(entity.get_body())

    replay_data.append(data)


def create_replay(filename: str):
    """
    Save the full replay data to a JSON file for future playback.

    The file is stored in the "replay" directory using the given filename.

    Args:
        filename (str): Name of the output JSON file (without extension).
    """
    global replay_storage

    if not os.path.exists("replay"):
        os.makedirs("replay")

    with open(f"replay/{filename}.json", "w") as f:
        json.dump(replay_storage, f)


def play_replay(replay_file: str, ep: int = -1):
    """
    Loads and replays the recorded gameplay from the JSON file.

    Renders each step of each episode with a short delay to simulate playback.
    """
    with open(replay_file, "r") as f:
        all_replay = json.load(f)

    if ep - 1 >= len(all_replay):
        print("Episode {} out of {}".format(ep, len(all_replay)))
        return

    if ep > 0:
        all_replay = [all_replay[ep - 1]]

    for i, episode in enumerate(all_replay):
        for replay in episode:
            game = Game()

            game.set_snake(replay["head"], replay["body"])
            game.set_apples(replay["apples"])

            title = f"Episode {str(i)}\n\n{replay['direction']}"

            game.get_world().render(title)
            time.sleep(0.3)
