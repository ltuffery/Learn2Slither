import csv
import time
import random
from engine.direction import Direction
from engine.game import Game
from engine.exception.gameover import GameOver
from ai.utils import action


Q = {}
past_configs = set()
loop_threshold = 15
loop_counter = 0


def serialize_snake_state(snake, action):
    """
    Serialize the snake's state for loop detection.

    Args:
        snake: The current snake instance.
        action: The last action taken.

    Returns:
        tuple: A unique representation of the snake's state.
    """
    head = (snake.get_x(), snake.get_y())
    body = tuple(snake.get_body())
    return head, body, action


def detect_loop(snake, action):
    """
    Detects if the snake is in a repeating loop.

    Args:
        snake: The current snake instance.
        action: The last action taken.

    Returns:
        bool: True if a loop is detected, False otherwise.
    """
    global loop_counter

    config = serialize_snake_state(snake, action)

    if config in past_configs:
        loop_counter += 1
    else:
        loop_counter = 0
        past_configs.add(config)

    return loop_counter > loop_threshold


def break_loop(snake, world, current_direction):
    """
    Tries to escape a detected loop by choosing a safe direction.

    Args:
        snake: The current snake instance.
        world: The game world.
        current_direction: The index of the current direction.

    Returns:
        Direction: A safe direction to break the loop.
    """
    safe_directions = []

    for d in Direction:
        if d == list(Direction)[current_direction]:
            continue

        nx = snake.get_x() + d.value[0]
        ny = snake.get_y() + d.value[1]

        if (nx, ny) in world.get_empty_locations():
            safe_directions.append(d)

    if safe_directions:
        return random.choice(safe_directions)

    return list(Direction)[current_direction].opposite()


def load_Q(f):
    with open(f, "r") as file:
        data = csv.DictReader(file)

        for row in data:
            state = eval(row['State'])
            a = Direction[row['Action']].index

            Q[(state, a)] = float(row['Q_Value'])


def play(q_file: str, visual: bool, step: bool) -> int:
    try:
        load_Q(q_file)
    except KeyError:
        print("Q file format not recognized")
        exit(1)

    is_last = False
    game = Game()
    past_configs.clear()

    game.start()

    snake = game.get_snake()

    while not is_last:
        s = snake.get_state()
        a = action(Q, s, 0.0)

        if detect_loop(snake, a):
            a = break_loop(snake, game.get_world(), a).index

        try:
            snake.move(list(Direction)[a])
        except GameOver:
            is_last = True

        if visual or step:
            game.get_world().render()

            if not step:
                time.sleep(0.3)
            elif not is_last:
                input("Press enter to continue...")

    return snake.get_size()
