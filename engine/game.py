from engine.world import World
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType


class Game:
    """
    Manages the setup, state, and entities of the Snake game.

    This class handles the game world, the player-controlled snake,
    and spawning of apples within the environment.

    Attributes:
        __world (World): The game world that contains all entities.
        __snake (Snake): The snake instance controlled by the game logic.
    """

    def __init__(self):
        """
        Initializes a Game instance without starting the game.

        The world is initialized, and the snake is set to None.
        """
        self.__world: World = World()
        self.__snake: Snake = Snake(self.__world)

    def start(self) -> None:
        """
        Starts or resets the game.

        Initializes the world and places the snake and two apples
        (one green and one red) at the starting position (0, 0).
        """
        self.__world = World()
        self.__snake = Snake(self.__world)

        self.__world.spawn_entity(self.__snake)
        self.__world.spawn_entity(Apple(AppleType.GREEN))
        self.__world.spawn_entity(Apple(AppleType.GREEN))
        self.__world.spawn_entity(Apple(AppleType.RED))

    def get_snake(self) -> Snake:
        """
        Retrieves the snake instance currently used in the game.

        Returns:
            Snake: The snake entity controlled in the game.
        """
        return self.__snake

    def get_world(self) -> World:
        """
        Retrieves the world instance used in the game.

        Returns:
            World: The current game world.
        """
        return self.__world

    def set_snake(self, head: tuple[int, int], body: list[tuple]) -> None:
        """
        Manually sets the snake's position and body segments in the world.

        Useful for testing or restoring a saved state.

        Args:
            head (tuple[int, int]): The (x, y) coordinates of the snake's head.
            body (list[tuple[int, int]]): A list of (x, y) tuples representing
                                          the snake's body segments.
        """
        self.__snake = Snake(self.__world)
        self.__snake.set_x(head[0])
        self.__snake.set_y(head[1])
        self.__snake.set_body(body)

        self.__world.add_entity(self.__snake)

    def set_apples(self, apples: list[tuple[int, int, bool]]) -> None:
        """
        Manually places apples in the world.

        Each apple is defined by its position and type.

        Args:
            apples (list[tuple[int, int, bool]]): A list of tuples,
                each representing an apple as (x, y, is_green), where
                `is_green` is a boolean indicating whether the apple is green.
        """
        for apple in apples:
            apple_type = AppleType.GREEN if apple[2] else AppleType.RED
            apple_obj = Apple(self.__world, apple_type)

            apple_obj.set_x(apple[0])
            apple_obj.set_y(apple[1])

            self.__world.add_entity(apple_obj)
