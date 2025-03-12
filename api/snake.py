from api.direction import Direction
from api.exception.engame import EndGameException
import copy

class SnakeBody:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y
    
    def move(self, x: int, y: int):
        self.__x = x
        self.__y = y

class Snake:
    def __init__(self, world, x: int, y: int, direction: Direction):
        self.__x = x
        self.__y = y
        self.__body: list[SnakeBody] = []
        self.__world = world

        for i in range(3):
            self.__body.append(
                SnakeBody(
                    x + direction.value[0] + i if direction.value[0] != 0 else x,
                    y + direction.value[1] + i if direction.value[1] != 0 else y
                )
            )
    
    def move(self, direction: Direction):
        x, y = direction.value
        info = self.__world.get_location(self.__x + x, self.__y + y)

        if not info.is_passable():
            raise EndGameException("End game")

        self.__x += x
        self.__y += y

        for i, body in reversed(list(enumerate(self.__body))):
            if i == 0:
                body.move(self.__x - x, self.__y - y)
            else:
                last = self.__body[i - 1]

                body.move(last.get_x(), last.get_y())

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y
    
    def get_body(self) -> list[SnakeBody]:
        return self.__body