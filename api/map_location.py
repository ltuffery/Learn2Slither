class MapLocation:
    def __init__(self, x: int, y: int, is_passable: bool):
        self.__x = x
        self.__y = y
        self.__is_passable = is_passable

    def is_passable(self) -> bool:
        return self.__is_passable

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y
