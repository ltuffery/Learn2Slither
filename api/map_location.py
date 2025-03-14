from api.entity.entity import Entity


class MapLocation:
    """
    Represents a specific location on the game map.

    Attributes:
        __x (int): The X-coordinate of the location.
        __y (int): The Y-coordinate of the location.
        __is_wall (bool): Indicates whether the location is a wall.
        __entity (Entity | None): The entity present at the location, if any.
    """

    def __init__(self, x: int, y: int, is_wall: bool, entity: Entity | None):
        """
        Initializes a map location with coordinates and passability status.

        Args:
            x (int): The X-coordinate of the location.
            y (int): The Y-coordinate of the location.
            is_wall (bool): Whether the location is a wall (not passable).
            entity (Entity | None): The entity at the location, or None if
            there is no entity.
        """
        self.__x = x
        self.__y = y
        self.__is_wall = is_wall
        self.__entity = entity

    def is_wall(self) -> bool:
        """
        Checks if the location is a wall (not passable).

        Returns:
            bool: True if the location is a wall, False otherwise.
        """
        return self.__is_wall

    def get_x(self) -> int:
        """
        Returns the X-coordinate of the location.

        Returns:
            int: The X-coordinate.
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the Y-coordinate of the location.

        Returns:
            int: The Y-coordinate.
        """
        return self.__y

    def get_entity(self) -> Entity | None:
        """
        Returns the entity at the location, if any.

        Returns:
            Entity | None: The entity at the location, or None if there
            is no entity.
        """
        return self.__entity
