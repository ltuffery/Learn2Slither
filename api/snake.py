from abc import abstractmethod
from api.direction import Direction


class SnakeInterface:
    """
    Defines the interface for a Snake entity in the game.

    This interface enforces the implementation of movement and vision
    methods for a Snake.
    """

    @abstractmethod
    def move(self, direction: Direction) -> None:
        """
        Moves the snake in the specified direction.

        Args:
            direction (Direction): The direction in which the snake should
            move.
        """
        pass

    @abstractmethod
    def see(self) -> list[list[str]]:
        """
        Provides the snake's current field of view as a 2D grid.

        Returns:
            list[list[str]]: A 2D list representing what the snake can see
            around it.
        """
        pass
