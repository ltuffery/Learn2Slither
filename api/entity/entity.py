from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def set_x(self, x: int) -> None:
        self.__x = x

    def set_y(self, y: int) -> None:
        self.__y = y

    @abstractmethod
    def get_char(self) -> str:
        pass

    def __str__(self):
        return self.get_char()
