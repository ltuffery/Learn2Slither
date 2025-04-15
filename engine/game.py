from engine.world import World
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType
from engine.direction import Direction


class Game:
    """
    Manages the setup and lifecycle of the Snake game.

    Attributes:
        __world (World): The game world where entities are placed.
        __snake (Snake): The snake controlled during the game.
    """

    def __init__(self):
        """
        Initializes the Game instance without starting the game.
        """
        self.__world: World = World()
        self.__snake: Snake = None  # Corrected type hint from World to Snake

    def start(self) -> None:
        """
        Starts the game by creating the world, initializing the snake,
        and spawning apples in the world.
        """
        self.__world = World()
        self.__snake = Snake(self.__world, 0, 0, Direction.EAST)

        self.__world.spawn_entity(self.__snake)
        self.__world.spawn_entity(Apple(self.__world, 0, 0, AppleType.GREEN))
        self.__world.spawn_entity(Apple(self.__world, 0, 0, AppleType.RED))

    def get_snake(self) -> Snake:
        """
        Returns the snake instance currently used in the game.

        Returns:
            SnakeInterface: The snake object implementing SnakeInterface.
        """
        return self.__snake
    
    def get_world(self) -> World:
        return self.__world
    
    def set_snake(self, head: tuple[int, int], body: list[tuple[int, int]]):
        self.__snake = Snake(self.__world, head[0], head[1], Direction.EAST)

        self.__snake.set_body(body)

        self.__world.add_entity(self.__snake)
    
    def set_apples(self, apples: list[tuple[int, int, bool]]):
        for apple in apples:
            if apple[2] is True:
                type = AppleType.GREEN
            else:
                type = AppleType.RED

            self.__world.add_entity(Apple(self.__world, apple[0], apple[1], type))
