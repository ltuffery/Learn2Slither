from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.apple import Apple
from api.world import World


class SnakeBody:
    """
    Represents a segment of a snake's body in a game.

    Attributes:
        __x (int): The X-coordinate of the body segment.
        __y (int): The Y-coordinate of the body segment.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes a body segment of the snake at a specific position.

        Args:
            x (int): The initial X position.
            y (int): The initial Y position.
        """
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        """
        Returns the X-coordinate of the body segment.

        Returns:
            int: The X-coordinate.
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the Y-coordinate of the body segment.

        Returns:
            int: The Y-coordinate.
        """
        return self.__y

    def move(self, x: int, y: int):
        """
        Moves the body segment to a new position.

        Args:
            x (int): The new X position.
            y (int): The new Y position.
        """
        self.__x = x
        self.__y = y


class Snake:
    """
    Represents a snake in the game, which moves, grows, and interacts with the
    world.

    Attributes:
        __x (int): The X-coordinate of the snake's head.
        __y (int): The Y-coordinate of the snake's head.
        __body (list[SnakeBody]): A list representing the snake's body
        segments.
        __world (World): The game world where the snake exists.
        __last_direction (Direction): The last movement direction of the snake.
    """

    def __init__(self, world: World, x: int, y: int, direction: Direction):
        """
        Initializes a snake in the given world at a specific position and
        direction.

        Args:
            world (World): The game world where the snake exists.
            x (int): The initial X position of the snake's head.
            y (int): The initial Y position of the snake's head.
            direction (Direction): The initial movement direction of the snake.
        """
        self.__x = x
        self.__y = y
        self.__body: list[SnakeBody] = []
        self.__world = world
        self.__last_direction = direction

        dir_x, dir_y = direction.value

        # Create the initial body of the snake (3 segments)
        for i in range(3):
            x += dir_x
            y += dir_y

            self.__body.append(SnakeBody(x, y))
            self.__world.spaw_entity(self.__body[-1])

    def move(self, direction: Direction):
        """
        Moves the snake in the given direction. If the new location is not
        passable, the game ends.

        Args:
            direction (Direction): The direction in which the snake should
            move.

        Raises:
            GameOver: If the snake collides with an obstacle or itself.
        """
        x, y = direction.value
        info = self.__world.get_location(self.__x + x, self.__y + y)

        if not info.is_passable():
            raise GameOver("End game")

        self.__x += x
        self.__y += y
        self.__last_direction = direction

        # Move the body segments following the head
        for i, body in reversed(list(enumerate(self.__body))):
            if i == 0:
                body.move(self.__x - x, self.__y - y)
            else:
                last = self.__body[i - 1]
                body.move(last.get_x(), last.get_y())

    def eat(self, apple: Apple):
        """
        Handles the snake eating an apple. The snake grows if the apple is
        green,
        otherwise, it loses a segment.

        Args:
            apple (Apple): The apple that the snake is eating.

        Raises:
            GameOver: If the snake loses its last segment.
        """
        if apple.is_green():
            x, y = self.__last_direction
            last_body = self.__body[-1]

            self.__body.append(
                SnakeBody(
                    last_body.get_x() + x,
                    last_body.get_y() + y
                )
            )
        else:
            if len(self.__body) == 0:
                raise GameOver("End game")

            del self.__body[-1]

    def size(self) -> int:
        """
        Returns the total size of the snake, including the head and body
        segments.

        Returns:
            int: The total number of segments in the snake.
        """
        return len(self.__body) + 1

    def get_x(self) -> int:
        """
        Returns the X-coordinate of the snake's head.

        Returns:
            int: The X position of the snake's head.
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the Y-coordinate of the snake's head.

        Returns:
            int: The Y position of the snake's head.
        """
        return self.__y

    def get_body(self) -> list[SnakeBody]:
        """
        Returns the list of body segments of the snake.

        Returns:
            list[SnakeBody]: The body segments of the snake.
        """
        return self.__body
