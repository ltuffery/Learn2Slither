from enum import Enum


class Direction(Enum):
    NORTH = (0, -1)
    SUD = (0, 1)
    EAST = (1, 0)
    WEAST = (-1, 0)

    def opposite(self):
        if self == Direction.NORTH:
            return Direction.SUD
        elif self == Direction.SUD:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEAST
        else:
            return Direction.EAST
