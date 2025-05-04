from engine.world import World
from engine.direction import Direction
from engine.exception.gameover import GameOver
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

world = World()
snake = Snake(world)

world.spawn_entity(snake)
world.spawn_entity(Apple(world, AppleType.GREEN))
world.spawn_entity(Apple(world, AppleType.GREEN))
world.spawn_entity(Apple(world, AppleType.RED))

while True:
    world.render()

    try:
        key = input("Move (W/A/S/D) : ").lower()
    except Exception:
        continue

    if key == 'q':
        print('Quitting the program')
        break

    try:
        if key == 'w':
            snake.move(Direction.NORTH)
        elif key == 's':
            snake.move(Direction.SOUTH)
        elif key == 'a':
            snake.move(Direction.WEST)
        elif key == 'd':
            snake.move(Direction.EAST)
    except GameOver:
        print("Good bye !")
        break
