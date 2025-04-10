from engine.world import World
from engine.direction import Direction
from engine.exception.gameover import GameOver
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

world = World()
snake = Snake(world, 5, 5, Direction.SOUTH)
green_apple = Apple(world, 2, 2, AppleType.GREEN)
red_apple = Apple(world, 2, 2, AppleType.RED)

world.spawn_entity(snake)
world.spawn_entity(green_apple)
world.spawn_entity(red_apple)

while True:
    world.render()

    key = input("Move (W/A/S/D) : ").lower()

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
