from api.world import World
from api.direction import Direction
import keyboard

world = World()
snake = world.create_snake()

while True:
    if keyboard.read_key() == 'q':
        print('Quitting the program')
        break
    if keyboard.read_key() == 'w':
        snake.move(Direction.NORTH)
    elif keyboard.read_key() == 's':
        snake.move(Direction.SUD)
    elif keyboard.read_key() == 'a':
        snake.move(Direction.WEAST)
    elif keyboard.read_key() == 'd':
        snake.move(Direction.EAST)