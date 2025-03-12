from snake import Snake
from map_location import MapLocation
import sys

class World:
    def __init__(self, heigth=10, width=10):
        self.__world: list = []
        self.__heigth: int = heigth
        self.__width: int = width
        self.__entities: list[Snake] = []

        self.__make_world()
    
    def __make_world(self) -> None:
        for i in range(self.__heigth + 2):
            if i == 0 or i == self.__heigth + 1:
                self.__world.append(['*' for _ in range(self.__width + 2)])
                continue

            ceil: list = ['*']

            for _ in range(self.__width):
                ceil.append(' ')

            ceil.append('*')
            self.__world.append(ceil)

    def get_location(self, x: int, y: int):
        if y > len(self.__world) or x > len(self.__world[y]):
            raise Exception('Invalid y') # TODO: Write exception message
        
        return MapLocation(x, y, self.__world[y][x] == ' ')
    
    def create_snake(self) -> Snake:
        snake = Snake(self, 2, 2)

        self.__entities.append(snake)

        return snake

    def render(self):
        sys.stdout.write("\033[H")
        sys.stdout.write("\033[J")

        world = self.__world

        for i, entity in enumerate(self.__entities):
            world[entity.get_y()][entity.get_x()] = '#'

        for i, line in enumerate(world):
            print("".join(line))

        sys.stdout.flush()
            