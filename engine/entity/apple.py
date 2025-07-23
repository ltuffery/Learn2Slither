from __future__ import annotations  # Enables postponed evaluation of type annotations
from enum import Enum

import engine.settings as settings
from engine.entity.entity import Entity


class AppleType(Enum):
    """
    Enumeration representing the type of an apple in the game.

    Each enum member corresponds to a specific type of apple (Red or Green)
    and holds the base reward value associated with that type.

    :cvar RED: Represents a red apple, associated with `settings.RED_APPLE_PENALTY`.
    :vartype RED: AppleType
    :cvar GREEN: Represents a green apple, associated with `settings.GREEN_APPLE_BONUS`.
    :vartype GREEN: AppleType
    """
    RED = settings.RED_APPLE_PENALTY
    GREEN = settings.GREEN_APPLE_BONUS


class Apple(Entity):
    """
    Represents an apple entity that can be either red or green.

    Red apples typically decrease the snake's size, while green apples
    make it grow. An apple's type is determined at its creation. Its
    position is managed externally by the `World` class.

    :ivar __apple_type: The type of the apple (RED or GREEN).
    :vartype __apple_type: AppleType
    """

    def __init__(self, apple_type: AppleType):
        """
        Initializes an Apple instance with a specified type.

        The apple's position (x, y) is initially set to (0, 0) by the
        base `Entity` constructor and should be updated explicitly
        (e.g., by `World.spawn_entity()` which calls `teleport`).

        :param apple_type: The type of apple (red or green).
        :type apple_type: AppleType
        """
        super().__init__()
        self.__apple_type: AppleType = apple_type

    def is_green(self) -> bool:
        """
        Determines whether the apple is a green apple.

        :return: True if the apple is green, False otherwise.
        :rtype: bool
        """
        return self.__apple_type == AppleType.GREEN

    def is_red(self) -> bool:
        """
        Determines whether the apple is a red apple.

        :return: True if the apple is red, False otherwise.
        :rtype: bool
        """
        return self.__apple_type == AppleType.RED

    def get_char(self) -> str:
        """
        Returns a colored character representation of the apple for display.

        The character and its color depend on the type of the apple (green or red),
        using values defined in `settings`. ANSI escape codes are used for coloring.

        :return: An ANSI-colored string representing the apple's character.
        :rtype: str
        """
        if self.is_green():
            return f"\033[32m{settings.GREEN_APPLE_CHAR}\033[0m"  # Green color
        return f"\033[31m{settings.RED_APPLE_CHAR}\033[0m"      # Red color

    def get_reward(self) -> int:
        """
        Retrieves the base reward value associated with this apple's type.

        This value directly comes from the `AppleType` enum, which uses
        reward values defined in `settings`.

        :return: The numeric reward value of the apple.
        :rtype: int
        """
        return self.__apple_type.value

    def render(self) -> list[tuple[str, int, int]]:
        """
        Generates a list of (character, x, y) tuples for rendering the apple
        on the game board.

        As an apple occupies only one grid cell, this list will contain a single tuple
        representing the apple's character and its current position.

        :return: A list containing a single tuple with:
                 - the character to display for the apple,
                 - the X coordinate of the apple,
                 - the Y coordinate of the apple.
        :rtype: list[tuple[str, int, int]]
        """
        return [(self.get_char(), self.get_x(), self.get_y())]