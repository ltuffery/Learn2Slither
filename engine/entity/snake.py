from engine.direction import Direction
from engine.exception.gameover import GameOver
from engine.entity.apple import Apple
from engine.world import World
from engine.entity.entity import Entity
import random
import engine.settings as settings
from collections import deque


class Snake(Entity):
    """
    Represents a snake in the game, which moves, grows, and interacts with the
    world.

    Attributes:
        __body (deque[tuple[int, int]]):
            Deque of tuples representing the snake's body segments.
        __world (World):
            The game world where the snake exists.
        __last_direction (Direction):
            The last movement direction of the snake.
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

        self.__body: deque[tuple[int, int]] = deque()
        self.__world: World = world
        self.__last_direction: Direction = direction

        dir_x, dir_y = direction.value

        # Create the initial body of the snake (3 segments)
        for _ in range(3):
            x += dir_x
            y += dir_y
            self.__body.append((x, y))

    def teleport(self, x: int, y: int) -> None:
        """
        Teleports the snake to a new position and resets its body direction.

        Args:
            x (int): The new X position.
            y (int): The new Y position.
        """
        super().teleport(x, y)

        new_body = deque()
        for _ in range(len(self.__body)):
            dir_name = self.__last_direction.name
            all_dir = [
                d for d in list(Direction) if d.name != dir_name
            ]
            is_empty = False

            while not is_empty and len(all_dir) > 0:
                self.__last_direction = random.choice(all_dir)
                dir_x, dir_y = self.__last_direction.value

                x += dir_x
                y += dir_y

                is_empty = self.__world.get_location(x, y).is_empty()

                if not is_empty or (x, y) in new_body:
                    is_empty = False
                    x -= dir_x
                    y -= dir_y
                    all_dir.remove(self.__last_direction)
                    continue

                new_body.append((x, y))

        self.__body = new_body

    def move(self, direction: Direction) -> int:
        """
        Moves the snake in the given direction. If the new location is not
        passable, the game ends.

        Args:
            direction (Direction): The direction in which the snake should
            move.

        Raises:
            GameOver: If the snake collides with an obstacle or itself.
        """
        reward = settings.EAT_NOTHING_REWARD
        x, y = direction.value
        new_x = self.get_x() + x
        new_y = self.get_y() + y
        info = self.__world.get_location(new_x, new_y)

        if info.is_wall() or (new_x, new_y) in self.__body:
            raise GameOver("End game")

        if isinstance(info.get_entity(), Apple):
            reward = self.eat(info.get_entity())

        self.set_x(new_x)
        self.set_y(new_y)
        self.__last_direction = direction

        # Move the body segments following the head
        self.__body.appendleft((self.get_x() - x, self.get_y() - y))
        self.__body.pop()

        return reward

    def eat(self, apple: Apple) -> int:
        """
        Handles the snake eating an apple.
        The snake grows if the apple is green, otherwise, it loses a segment.

        Args:
            apple (Apple): The apple that the snake is eating.

        Raises:
            GameOver: If the snake loses its last segment.
        """
        if apple.is_green():
            x, y = self.__last_direction.value

            if len(self.__body) > 0:
                last_body = self.__body[-1]
            else:
                last_body = self.get_position()

            # Grow the snake by adding a new body segment
            self.__body.append((last_body[0] + x, last_body[1] + y))
        else:
            if not self.__body:
                raise GameOver("End game")

            # Remove the last body segment
            self.__body.pop()

        apple.consume()

        return apple.get_reward()

    def size(self) -> int:
        """
        Returns the total size of the snake, including the head and body
        segments.

        Returns:
            int: The total number of segments in the snake.
        """
        return len(self.__body) + 1

    def get_state_at(self, x: int, y: int) -> str | None:
        """
        Returns the state of a given position in the game world.

        Args:
            x (int): The X-coordinate of the position.
            y (int): The Y-coordinate of the position.

        Returns:
            str | None: A character representing the state of the position:
                settings.WALL_CHAR for a wall,
                '.' for a green apple,
                '~' for a red apple,
                'H' for the snake's head,
                'S' for the snake's body,
                None if the position is empty.
        """
        info = self.__world.get_location(x, y)

        if info.is_wall():
            return settings.WALL_CHAR

        if isinstance(info.get_entity(), Apple):
            apple: Apple = info.get_entity()
            if apple.is_green():
                return settings.GREEN_APPLE_CHAR
            else:
                return settings.RED_APPLE_CHAR

        if x == self.get_x() and y == self.get_y():
            return settings.SNAKE_HEAD_CHAR

        if (x, y) in self.__body:
            return settings.SNAKE_SEGMENT_CHAR

        return None

    def see(self) -> list[list[str]]:
        """
        Returns a 2D grid representation of the world from the snake's
        perspective.

        The grid contains the state of each position in the game world.

        Returns:
            list[list[str]]: A 2D list where each element represents a position
            in the world as returned by `get_state_at()`.
        """
        height = self.__world.get_height() + 2
        width = self.__world.get_width() + 2
        state = [[None for _ in range(width)] for _ in range(height)]

        for x in range(width):
            state[self.get_y()][x] = self.get_state_at(x, self.get_y())

        for y in range(height):
            state[y][self.get_x()] = self.get_state_at(self.get_x(), y)

        return state

    def get_state(self) -> list[bool]:
        """
        Returns a boolean list representing the game state from the snake's
        perspective.

        The list contains 12 booleans:
            - 0-1: Green apple on the left/right
            - 2-3: Green apple on the top/bottom
            - 4-5: Red apple on the left/right
            - 6-7: Red apple on the top/bottom
            - 8-11: Wall or body on left, right, top, bottom

        Returns:
            list[bool]: The encoded state of the environment.
        """
        state = [False] * 12
        see = self.see()

        for x in range(self.get_x()):
            if see[self.get_y()][x] == settings.GREEN_APPLE_CHAR:
                state[0 + int(x > self.get_x())] = True
            elif see[self.get_y()][x] == settings.RED_APPLE_CHAR:
                state[4 + int(x > self.get_x())] = True

        for y in range(self.get_y()):
            if see[y][self.get_x()] == settings.GREEN_APPLE_CHAR:
                state[2 + int(y > self.get_y())] = True
            elif see[y][self.get_x()] == settings.RED_APPLE_CHAR:
                state[6 + int(y > self.get_y())] = True

        not_passable = [settings.WALL_CHAR, settings.SNAKE_SEGMENT_CHAR]

        if see[self.get_y()][self.get_x() - 1] in not_passable:
            state[8] = True
        if see[self.get_y()][self.get_x() + 1] in not_passable:
            state[9] = True
        if see[self.get_y() - 1][self.get_x()] in not_passable:
            state[10] = True
        if see[self.get_y() + 1][self.get_x()] in not_passable:
            state[11] = True

        return state

    def get_body(self) -> deque[tuple[int, int]]:
        """
        Returns the list of body segments of the snake.

        Returns:
            deque[tuple[int, int]]: The body segments of the snake.
        """
        return self.__body

    def set_body(self, body: list[tuple[int, int]]):
        self.__body = deque(body)

    def get_char(self) -> str:
        """
        Returns the character representation of the snake, colored for terminal
        output.

        Returns:
            str: A string representing the snake, colored in yellow.
        """
        return f"\033[33m{settings.SNAKE_HEAD_CHAR}\033[0m"

    def render(self) -> list[tuple[str, int, int]]:
        """
        Renders the snake's head and body in the world.

        Returns:
            list[tuple[str, int, int]]: A list containing tuples with:
                - the character to display,
                - the X coordinate,
                - the Y coordinate.
        """
        render = super().render()

        for body in self.__body:
            render.append((settings.SNAKE_SEGMENT_CHAR, body[0], body[1]))

        return render
