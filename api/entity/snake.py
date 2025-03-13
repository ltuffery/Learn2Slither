from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.apple import Apple
from api.world import World
from api.entity.entity import Entity


class SnakeBody(Entity):
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
            x (int): The initial X position of the body segment.
            y (int): The initial Y position of the body segment.
        """
        super().__init__(x, y)

    def move(self, x: int, y: int):
        """
        Moves the body segment to a new position.

        Args:
            x (int): The new X position of the body segment.
            y (int): The new Y position of the body segment.
        """
        self.set_x(x)
        self.set_y(y)

    def get_char(self) -> str:
        """
        Returns the character representation of a body segment for rendering in
        the terminal.

        Returns:
            str: The character "#" representing the body segment.
        """
        return "#"


class Snake(Entity):
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
        super().__init__(x, y)

        self.__body: list[SnakeBody] = []
        self.__world: World = world
        self.__last_direction: Direction = direction

        dir_x, dir_y = direction.value

        # Create the initial body of the snake (3 segments)
        for i in range(3):
            x += dir_x
            y += dir_y

            self.__body.append(SnakeBody(x, y))
            self.__world.spawn_entity(self.__body[-1])

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
        info = self.__world.get_location(self.get_x() + x, self.get_y() + y)

        if not info.is_passable():
            raise GameOver("End game")

        self.set_x(self.get_x() + x)
        self.set_y(self.get_y() + y)
        self.__last_direction = direction

        # Move the body segments following the head
        for i, body in reversed(list(enumerate(self.__body))):
            if i == 0:
                body.move(self.get_x() - x, self.get_y() - y)
            else:
                last = self.__body[i - 1]
                body.move(last.get_x(), last.get_y())

    def eat(self, apple: Apple):
        """
        Handles the snake eating an apple. The snake grows if the apple is
        green, otherwise, it loses a segment.

        Args:
            apple (Apple): The apple that the snake is eating.

        Raises:
            GameOver: If the snake loses its last segment.
        """
        if apple.is_green():
            x, y = self.__last_direction
            last_body = self.__body[-1]

            # Grow the snake by adding a new body segment
            self.__body.append(
                SnakeBody(
                    last_body.get_x() + x,
                    last_body.get_y() + y
                )
            )
        else:
            if len(self.__body) == 0:
                raise GameOver("End game")

            # Remove the last body segment
            del self.__body[-1]

    def size(self) -> int:
        """
        Returns the total size of the snake, including the head and body
        segments.

        Returns:
            int: The total number of segments in the snake.
        """
        return len(self.__body) + 1

    def get_body(self) -> list[SnakeBody]:
        """
        Returns the list of body segments of the snake.

        Returns:
            list[SnakeBody]: The body segments of the snake.
        """
        return self.__body

    def get_char(self) -> str:
        """
        Returns the character representation of the snake, colored for
        terminal output.

        Returns:
            str: A string representing the snake, colored in yellow.
        """
        return "\033[33m#\033[0m"
