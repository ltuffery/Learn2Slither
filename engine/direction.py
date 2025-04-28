from enum import Enum


class Direction(Enum):
    """
    Represents the possible movement directions in the game.

    Attributes:
        NORTH (tuple[int, int]): Moves upward (0, -1).
        SOUTH (tuple[int, int]): Moves downward (0, 1).
        EAST (tuple[int, int]): Moves right (1, 0).
        WEST (tuple[int, int]): Moves left (-1, 0).
    """

    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def opposite(self) -> "Direction":
        """
        Returns the opposite direction.

        Returns:
            Direction: The opposite movement direction.
        """
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEST
        else:
            return Direction.EAST
    
    @property
    def index(self):
        return list(Direction).index(self)
