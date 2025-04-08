from enum import Enum
from engine.entity.entity import Entity
from engine.world import World
import engine.settings as settings


class AppleType(Enum):
    """
    Enumeration representing the type of an apple in the game.

    The value of each enum corresponds to the reward value associated
    with that type of apple.
    """
    RED = settings.RED_APPLE_REWARD
    GREEN = settings.GREEN_APPLE_REWARD


class Apple(Entity):
    """
    Represents an apple entity that can be either red or green.

    Red apples decrease the snake's size, while green apples make it grow.

    Attributes:
        __world (World): The game world in which the apple exists.
        __apple_type (AppleType): The type of the apple (RED or GREEN).
    """

    def __init__(self, world: World, x: int, y: int, apple_type: AppleType):
        """
        Initializes the apple with a given type and position.

        Args:
            world (World): The game world instance where the apple is placed.
            x (int): The X-coordinate of the apple's initial position.
            y (int): The Y-coordinate of the apple's initial position.
            apple_type (AppleType): The type of apple (red or green).
        """
        super().__init__(x, y)
        self.__world = world
        self.__apple_type = apple_type

    def is_green(self) -> bool:
        """
        Determines whether the apple is green.

        Returns:
            bool: True if the apple is green, False otherwise.
        """
        return self.__apple_type == AppleType.GREEN

    def is_red(self) -> bool:
        """
        Determines whether the apple is red.

        Returns:
            bool: True if the apple is red, False otherwise.
        """
        return self.__apple_type == AppleType.RED

    def get_char(self) -> str:
        """
        Returns a colored character representation of the apple for display.

        The color depends on the type of the apple (green or red).

        Returns:
            str: ANSI-colored string representing the apple.
        """
        if self.is_green():
            return f"\033[32m{settings.GREEN_APPLE_CHAR}\033[0m"

        return f"\033[31m{settings.RED_APPLE_CHAR}\033[0m"

    def consume(self) -> None:
        """
        Handles the apple being consumed.

        The apple is removed from the game world and respawned immediately.
        """
        self.__world.remove_entity(self)
        self.__world.spawn_entity(self)

    def get_reward(self) -> int:
        """
        Retrieves the reward value associated with the apple type.

        Returns:
            int: The numeric reward value of the apple.
        """
        return self.__apple_type.value
