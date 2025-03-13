from enum import Enum


class Direction(Enum):
    NORTH = (0, -1)
    SUD = (0, 1)
    EAST = (1, 0)
    WEAST = (-1, 0)
