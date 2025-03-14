from api.world import World
from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.snake import Snake
from api.entity.apple import Apple, AppleType

world = World()
snake = Snake(world, 5, 5, Direction.SOUTH)
green_apple = Apple(world, 2, 2, AppleType.GREEN)

world.spawn_entity(snake)
world.spawn_entity(green_apple)

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
