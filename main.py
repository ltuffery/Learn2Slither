from api.world import World
from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.snake import Snake

world = World()
snake = Snake(world, 5, 5, Direction.SUD)

world.spaw_entity(snake)

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
            snake.move(Direction.SUD)
        elif key == 'a':
            snake.move(Direction.WEAST)
        elif key == 'd':
            snake.move(Direction.EAST)
    except GameOver:
        print("Good bye !")
        break
