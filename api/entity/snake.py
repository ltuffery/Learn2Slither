from api.direction import Direction
from api.exception.gameover import GameOver
from api.entity.apple import Apple
from api.world import World
from api.entity.entity import Entity
import random


class Snake(Entity):
    """
    Represents a snake in the game, which moves, grows, and interacts with the
    world.

    Attributes:
        __x (int): The X-coordinate of the snake's head.
        __y (int): The Y-coordinate of the snake's head.
        __body (list[tuple[int, int]]): A list representing the snake's body
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

        self.__body: list[tuple[int, int]] = []
        self.__world: World = world
        self.__last_direction: Direction = direction

        dir_x, dir_y = direction.value

        # Create the initial body of the snake (3 segments)
        for _ in range(3):
            x += dir_x
            y += dir_y
            self.__body.append((x, y))
    
    def teleport(self, x, y):
        super().teleport(x, y)

        for i in range(len(self.__body)):
            del self.__body[i]

            self.__last_direction = random.choice([ x for x in list(Direction) if x.name != self.__last_direction.name ])
            dir_x, dir_y = self.__last_direction.value

            x += dir_x
            y += dir_y

            self.__body.insert(i, (x, y))

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

        if info.is_wall():
            raise GameOver("End game")

        if (self.get_x() + x, self.get_y() + y) in self.__body:
            raise GameOver("End game")

        if isinstance(info.get_entity(), Apple):
            self.eat(info.get_entity())

        self.set_x(self.get_x() + x)
        self.set_y(self.get_y() + y)
        self.__last_direction = direction

        # Move the body segments following the head
        self.__body.insert(0, (self.get_x() - x, self.get_y() - y))
        del self.__body[-1]

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
            x, y = self.__last_direction.value
            last_body = self.__body[-1]

            # Grow the snake by adding a new body segment
            self.__body.append((last_body[0] + x, last_body[1] + y))
        else:
            if len(self.__body) == 0:
                raise GameOver("End game")

            # Remove the last body segment
            del self.__body[-1]
        
        apple.consume()

    def size(self) -> int:
        """
        Returns the total size of the snake, including the head and body
        segments.

        Returns:
            int: The total number of segments in the snake.
        """
        return len(self.__body) + 1

    def get_body(self) -> list[tuple[int, int]]:
        """
        Returns the list of body segments of the snake.

        Returns:
            list[tuple[int, int]]: The body segments of the snake.
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

    def render(self):
        """
        Renders the snake and its body in the world.

        Returns:
            list: A list containing the snake's head and body positions.
        """
        render = super().render()
        [render.append(("#", body[0], body[1])) for body in self.__body]

        return render
