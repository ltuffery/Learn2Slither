from enum import Enum


class AppleType(Enum):
    """
    Enum representing the type of an apple.

    Attributes:
        RED (int): Represents a red apple.
        GREEN (int): Represents a green apple.
    """
    RED = 0
    GREEN = 1


class Apple:
    """
    Represents an apple in the game, which can be either red or green.

    Attributes:
        apple_type (AppleType): The type of the apple (RED or GREEN).
    """

    def __init__(self, apple_type: AppleType):
        """
        Initializes an apple with a specified type.

        Args:
            apple_type (AppleType): The type of the apple (RED or GREEN).
        """
        self.apple_type = apple_type

    def is_green(self) -> bool:
        """
        Checks if the apple is green.

        Returns:
            bool: True if the apple is green, False otherwise.
        """
        return self.apple_type == AppleType.GREEN

    def is_red(self) -> bool:
        """
        Checks if the apple is red.

        Returns:
            bool: True if the apple is red, False otherwise.
        """
        return self.apple_type == AppleType.RED
