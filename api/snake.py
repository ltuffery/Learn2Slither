from world import World
from direction import Direction

class Snake:
    def __init__(self, world: World, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__size = 1
        self.__world = world
    
    def move(self, direction: Direction):
        x, y = direction.value
        info = self.__world.get_location(x, y)

        if not info.is_passable():
            raise Exception("Not passable") # TODO: Write exception message

        self.__x += x
        self.__y += y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y