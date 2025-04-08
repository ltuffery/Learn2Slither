from engine.world import World
from engine.entity.snake import Snake, SnakeInterface
from engine.entity.apple import Apple, AppleType
from api.direction import Direction


class Game:
    def __init__(self):
        self.__world: World = None
        self.__snake: World = None

    def start(self):
        self.__world = World()
        self.__snake = Snake(self.__world, 0, 0, Direction.EAST)

        self.__world.spawn_entity(self.__snake)
        self.__world.spawn_entity(Apple(self.__world, 0, 0, AppleType.GREEN))
        self.__world.spawn_entity(Apple(self.__world, 0, 0, AppleType.RED))

    def get_snake(self) -> SnakeInterface:
        return self.__snake
