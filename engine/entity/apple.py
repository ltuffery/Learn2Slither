from enum import Enum
from engine.entity.entity import Entity
from engine.world import World


class AppleType(Enum):
    """
    Enum representing the type of an apple.

    Attributes:
        RED (int): Represents a red apple.
        GREEN (int): Represents a green apple.
    """
    RED = 0
    GREEN = 1


class Apple(Entity):
    """
    Represents an apple in the game, which can be either red or green.

    Attributes:
        apple_type (AppleType): The type of the apple (RED or GREEN).
    """

    def __init__(self, world: World, x: int, y: int, apple_type: AppleType):
        """
        Initializes an apple with a specified type and position.

        Args:
            x (int): The x-coordinate of the apple's position.
            y (int): The y-coordinate of the apple's position.
            apple_type (AppleType): The type of the apple (RED or GREEN).
        """
        super().__init__(x, y)

        self.__world = world
        self.__apple_type = apple_type

    def is_green(self) -> bool:
        """
        Checks if the apple is green.

        Returns:
            bool: True if the apple is green, False otherwise.
        """
        return self.__apple_type == AppleType.GREEN

    def is_red(self) -> bool:
        """
        Checks if the apple is red.

        Returns:
            bool: True if the apple is red, False otherwise.
        """
        return self.__apple_type == AppleType.RED

    def get_char(self) -> str:
        """
        Returns a character representation of the apple, colored based on
        its type.

        Returns:
            str: A string representing the apple with appropriate color
            formatting for the terminal.
        """
        if self.is_green():
            return "\033[32m@\033[0m"  # Green apple

        return "\033[31m@\033[0m"  # Red apple

    def consume(self):
        """
        Removes the apple from the world and respawns it.

        The apple is removed from the world and then spawned again at the
        same location.
        """
        self.__world.remove_entity(self)
        self.__world.spawn_entity(self)
