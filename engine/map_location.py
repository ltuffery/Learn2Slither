from engine.entity.entity import Entity


class MapLocation:
    """
    Represents a specific location on the game map.

    This class encapsulates the coordinates (x, y) of a point on the map,
    whether it's considered a wall, and if there's an entity present at that location.
    It provides methods to query these properties.

    :ivar __x: The X-coordinate of the location.
    :vartype __x: int
    :ivar __y: The Y-coordinate of the location.
    :vartype __y: int
    :ivar __is_wall: True if the location is a structural wall, False otherwise.
    :vartype __is_wall: bool
    :ivar __entity: The entity present at this location, or None if empty.
    :vartype __entity: Entity | None
    """

    def __init__(self, x: int, y: int, is_wall: bool, entity: Entity | None):
        """
        Initializes a map location with its coordinates, wall status, and
        any entity occupying it.

        :param x: The X-coordinate of the location.
        :type x: int
        :param y: The Y-coordinate of the location.
        :type y: int
        :param is_wall: Whether the location is a structural wall.
        :type is_wall: bool
        :param entity: The entity at the location, or None if there is no entity.
        :type entity: Entity | None
        """
        self.__x = x
        self.__y = y
        self.__is_wall = is_wall
        self.__entity = entity

    def is_wall(self) -> bool:
        """
        Checks if the location is a structural wall.

        :return: True if the location is a wall, False otherwise.
        :rtype: bool
        """
        return self.__is_wall

    def get_x(self) -> int:
        """
        Returns the X-coordinate of the location.

        :return: The X-coordinate.
        :rtype: int
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the Y-coordinate of the location.

        :return: The Y-coordinate.
        :rtype: int
        """
        return self.__y

    def get_entity(self) -> Entity | None:
        """
        Returns the entity at the location, if any.

        :return: The entity at the location, or None if there is no entity.
        :rtype: Entity | None
        """
        return self.__entity

    def is_empty(self) -> bool:
        """
        Checks if the location is empty (not a wall and no entity present).

        :return: True if the location is empty, False otherwise.
        :rtype: bool
        """
        return not self.__is_wall and self.__entity is None