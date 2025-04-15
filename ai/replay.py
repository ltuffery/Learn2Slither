from engine.game import Game
from engine.entity.apple import Apple
from engine.entity.snake import Snake
import json
import time

replay_storage = []
replay_data = []

def reset_replay():
    global replay_data
    global replay_storage

    if len(replay_data) > 0:
        replay_storage.append(replay_data)
    replay_data = []

def save_game_state(game: Game):
    global replay_data

    data = {
        "apples": []
    }

    for entity in game.get_world().get_entities():
        if isinstance(entity, Apple):
            data["apples"].append((entity.get_x(), entity.get_y(), entity.is_green()))
        elif isinstance(entity, Snake):
            data['head'] = entity.get_position()
            data['body'] = list(entity.get_body())
    
    replay_data.append(data)

def create_replay():
    global replay_storage

    with open("replay/replay.json", "w") as f:
        json.dump(replay_storage, f)

def play_replay():
    with open("replay/replay.json", "r") as f:
        all_replay = json.load(f)
    
    for i, episode in enumerate(all_replay):
        for replay in episode:
            game = Game()

            game.set_snake(replay["head"], replay["body"])
            game.set_apples(replay["apples"])

            game.get_world().render(f"Episode {str(i)}\n")
            time.sleep(0.3)