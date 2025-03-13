class MapLocation:
    """
    Represents a specific location on the game map.

    Attributes:
        __x (int): The X-coordinate of the location.
        __y (int): The Y-coordinate of the location.
        __is_passable (bool): Indicates whether the location is passable.
    """

    def __init__(self, x: int, y: int, is_passable: bool):
        """
        Initializes a map location with coordinates and passability status.

        Args:
            x (int): The X-coordinate of the location.
            y (int): The Y-coordinate of the location.
            is_passable (bool): Whether the location is passable.
        """
        self.__x = x
        self.__y = y
        self.__is_passable = is_passable

    def is_passable(self) -> bool:
        """
        Checks if the location is passable.

        Returns:
            bool: True if the location is passable, False otherwise.
        """
        return self.__is_passable

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
