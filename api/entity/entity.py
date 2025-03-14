from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Represents a game entity that has a position in the game world.

    Attributes:
        __x (int): The X-coordinate of the entity.
        __y (int): The Y-coordinate of the entity.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes an entity with specified coordinates.

        Args:
            x (int): The X-coordinate of the entity.
            y (int): The Y-coordinate of the entity.
        """
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        """
        Returns the X-coordinate of the entity.

        Returns:
            int: The X-coordinate of the entity.
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the Y-coordinate of the entity.

        Returns:
            int: The Y-coordinate of the entity.
        """
        return self.__y

    def get_position(self) -> tuple[int, int]:
        """
        Returns the position of the entity as a tuple of (x, y).

        Returns:
            tuple[int, int]: The position of the entity.
        """
        return (self.get_x(), self.get_y())

    def set_x(self, x: int) -> None:
        """
        Sets the X-coordinate of the entity.

        Args:
            x (int): The new X-coordinate.
        """
        self.__x = x

    def set_y(self, y: int) -> None:
        """
        Sets the Y-coordinate of the entity.

        Args:
            y (int): The new Y-coordinate.
        """
        self.__y = y

    def teleport(self, x: int, y: int) -> None:
        """
        Teleports the entity to a new position (x, y).

        Args:
            x (int): The new X-coordinate.
            y (int): The new Y-coordinate.
        """
        self.__x = x
        self.__y = y

    @abstractmethod
    def get_char(self) -> str:
        """
        Abstract method to return the character representation of the entity.

        Returns:
            str: The character representing the entity.
        """
        pass

    def render(self) -> list[tuple[str, int, int]]:
        """
        Renders the entity's character and position.

        Returns:
            list[tuple[str, int, int]]: A list containing a tuple of the
            entity's character and its coordinates (x, y).
        """
        return [(self.get_char(), self.get_x(), self.get_y())]

    def __str__(self):
        """
        Returns a string representation of the entity.

        Returns:
            str: The character representation of the entity.
        """
        return self.get_char()
