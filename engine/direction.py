from enum import Enum


class Direction(Enum):
    """
    Represents the possible movement directions in the game.

    Attributes:
        UP (tuple[int, int]): Moves upward (0, -1).
        DOWN (tuple[int, int]): Moves downward (0, 1).
        LEFT (tuple[int, int]): Moves right (1, 0).
        RIGHT (tuple[int, int]): Moves left (-1, 0).
    """

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    def opposite(self) -> "Direction":
        """
        Returns the opposite direction.

        Returns:
            Direction: The opposite movement direction.
        """
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT

    @property
    def index(self):
        """
        Returns the index of the current Direction instance.

        This property calculates the position of the current Direction
        in the list of all possible Direction values.

        Returns:
            int: The index of the Direction instance within the Direction
            enumeration.
        """
        return list(Direction).index(self)
