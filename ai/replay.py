from engine.game import Game
from engine.entity.apple import Apple
from engine.entity.snake import Snake
from engine.direction import Direction
import json
import time
import sys

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
    Captures and stores the current game state along with the snake's
    direction.

    Args:
        game (Game): The current game instance to record.
        direction (Direction): The direction in which the snake is currently
        moving.
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


def create_replay():
    """
    Saves the entire replay storage to a JSON file for later playback.

    The replay is saved to "replay/replay.json".
    """
    global replay_storage

    with open("replay/replay.json", "w") as f:
        json.dump(replay_storage, f)


def play_replay(ep: int = -1):
    """
    Loads and replays the recorded gameplay from the JSON file.

    Renders each step of each episode with a short delay to simulate playback.
    """
    with open("replay/replay.json", "r") as f:
        all_replay = json.load(f)

    if ep > -1:
        for replay in all_replay[ep]:
            game = Game()

            game.set_snake(replay["head"], replay["body"])
            game.set_apples(replay["apples"])

            title = f"Episode {str(ep)}\n\n{replay['direction']}"

            game.get_world().render(title)
            time.sleep(0.3)
        return

    for i, episode in enumerate(all_replay):
        for replay in episode:
            game = Game()

            game.set_snake(replay["head"], replay["body"])
            game.set_apples(replay["apples"])

            title = f"Episode {str(i)}\n\n{replay['direction']}"

            game.get_world().render(title)
            time.sleep(0.3)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            play_replay(int(sys.argv[1]))
        except ValueError:
            print("Bad argument")
    else:
        play_replay()
