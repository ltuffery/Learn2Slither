from enum import Enum


class AppleType(Enum):
    RED = 0
    GREEN = 1


class Apple:
    def __init__(self, apple_type: AppleType):
        self.apple_type = apple_type

    def is_green(self) -> bool:
        return self.apple_type == AppleType.GREEN

    def is_red(self) -> bool:
        return self.apple_type == AppleType.RED
