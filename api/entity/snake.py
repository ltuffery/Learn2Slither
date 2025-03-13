from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.apple import Apple
from api.world import World


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
    def __init__(self, world: World, x: int, y: int, direction: Direction):
        self.__x = x
        self.__y = y
        self.__body: list[SnakeBody] = []
        self.__world = world
        self.__last_direction = direction

        dir_x, dir_y = direction.value

        for i in range(3):
            x += dir_x
            y += dir_y

            self.__body.append(
                SnakeBody(x, y)
            )

            self.__world.spaw_entity(self.__body[-1])

    def move(self, direction: Direction):
        x, y = direction.value
        info = self.__world.get_location(self.__x + x, self.__y + y)

        if not info.is_passable():
            raise GameOver("End game")

        self.__x += x
        self.__y += y
        self.__last_direction = direction

        for i, body in reversed(list(enumerate(self.__body))):
            if i == 0:
                body.move(self.__x - x, self.__y - y)
            else:
                last = self.__body[i - 1]

                body.move(last.get_x(), last.get_y())

    def eat(self, apple: Apple):
        if apple.is_green():
            x, y = self.__last_direction
            last_body = self.__body[-1]

            self.__body.append(
                SnakeBody(
                    last_body.get_x() + x,
                    last_body.get_y() + y
                )
            )
        else:
            if len(self.__body) == 0:
                raise GameOver("End game")

            del self.__body[-1]

    def size(self):
        return len(self.__body) + 1

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_body(self) -> list[SnakeBody]:
        return self.__body
