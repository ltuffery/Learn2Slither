from engine.world import World
from engine.entity.snake import Snake, SnakeInterface
from engine.entity.apple import Apple, AppleType
from api.direction import Direction


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
        self.__world: World = None
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

    def get_snake(self) -> SnakeInterface:
        """
        Returns the snake instance currently used in the game.

        Returns:
            SnakeInterface: The snake object implementing SnakeInterface.
        """
        return self.__snake
