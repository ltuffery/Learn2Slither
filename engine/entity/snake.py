import random
from collections import deque

import engine.settings as settings
from engine.direction import Direction
from engine.entity.apple import Apple
from engine.entity.entity import Entity
from engine.exception.gameover import GameOver
from engine.world import World


class Snake(Entity):
    """
    Represents a snake in the game, which moves, grows, and interacts with the
    world.

    The snake's behavior is driven by an AI agent that receives
    a limited "vision" of its immediate surroundings.

    :ivar __body: Deque of tuples representing the snake's body segments.
    :vartype __body: deque[tuple[int, int]]
    :ivar __world: The game world where the snake exists.
    :vartype __world: World
    :ivar __last_direction: The last movement direction of the snake.
    :vartype __last_direction: Direction
    :ivar __is_dead: True if the snake is dead, False otherwise.
    :vartype __is_dead: bool
    """

    def __init__(self, world: World):
        """
        Initializes a snake in the given world at a specific position and
        direction.

        The snake starts with a length of 3 cells, placed randomly and
        contiguously on the board.

        :param world: The game world where the snake exists.
        :type world: World
        """
        super().__init__()

        self.__body: deque[tuple[int, int]] = deque()
        self.__world: World = world
        self.__last_direction: Direction = random.choice(list(Direction))
        self.__is_dead: bool = False

        # Initialize snake body (3 segments including the head)
        self._initialize_body()

    def _initialize_body(self) -> None:
        """
        Initializes the snake's body segments based on its initial head
        position and direction.
        """
        head_x, head_y = self.get_position()
        current_x, current_y = head_x, head_y

        for _ in range(settings.INITIAL_SNAKE_LENGTH - 1):
            # Try to place body segments contiguously in the last direction
            dir_x, dir_y = self.__last_direction.value
            current_x -= dir_x  # Move backwards from head to build body
            current_y -= dir_y

            # Basic check to ensure body stays within bounds (for initial spawn)
            if (
                not self.__world.is_within_bounds(current_x, current_y)
                or (current_x, current_y) in self.__body
                or (current_x, current_y) == (head_x, head_y)
            ):
                # If cannot place backwards, try another direction for remaining
                # segments. This part can be more robust depending on spawn logic.
                # For simplicity, if initial backward placement fails,
                # we'll just append at the current head's previous position.
                # A more sophisticated solution would retry finding valid
                # contiguous cells.
                fallback_x, fallback_y = self.__body[
                    -1
                ] if self.__body else (head_x, head_y)
                # Find an empty adjacent cell for the new segment
                found_valid_pos = False
                for d in Direction:
                    nx, ny = fallback_x + d.value[0], fallback_y + d.value[1]
                    if (
                        self.__world.is_within_bounds(nx, ny)
                        and self.__world.get_location(nx, ny).is_empty()
                        and (nx, ny) not in self.__body
                        and (nx, ny) != (head_x, head_y)
                    ):
                        self.__body.append((nx, ny))
                        found_valid_pos = True
                        break
                if not found_valid_pos:
                    # As a last resort, just duplicate the last segment or head
                    # This indicates a potential issue with initial placement logic
                    # if it cannot find 3 contiguous cells.
                    self.__body.append(self.__body[-1] if self.__body else (head_x, head_y))
            else:
                self.__body.append((current_x, current_y))

    def teleport(self, x: int, y: int) -> None:
        """
        Teleports the snake to a new position and reinitializes its body.
        The new body will be contiguous to the new head position.

        :param x: The new X position for the snake's head.
        :type x: int
        :param y: The new Y position for the snake's head.
        :type y: int
        """
        super().teleport(x, y)
        self.__body.clear()
        self._initialize_body()  # Re-initialize body relative to new head

    def move(self, direction: Direction) -> int:
        """
        Moves the snake in the given direction.
        Handles collisions with walls or itself, triggering a Game Over.
        Manages eating apples and adjusting snake length and rewards.

        :param direction: The direction in which the snake should move.
        :type direction: Direction
        :raises GameOver: If the snake collides with a wall or its own tail,
                          or if its length drops to 0.

        :return: The reward obtained from this move.
        :rtype: int
        """
        reward = settings.EAT_NOTHING_REWARD
        old_head_x, old_head_y = self.get_position()
        new_head_x, new_head_y = (
            old_head_x + direction.value[0],
            old_head_y + direction.value[1],
        )

        # Check for collisions with walls or self

        if (
            self.__world.get_location(new_head_x, new_head_y).is_wall()
            or (new_head_x, new_head_y) in self.__body
        ):
            self.__is_dead = True
            raise GameOver("Snake hit wall or itself. Game over!")

        # Check what's at the new head position
        entity_at_new_pos = self.__world.get_location(new_head_x, new_head_y).get_entity()

        if isinstance(entity_at_new_pos, Apple):
            reward = self.eat(entity_at_new_pos)
        
        if self.__body:
            self.__body.pop()
            self.__body.appendleft((old_head_x, old_head_y))

        # Update snake's head position
        self.set_x(new_head_x)
        self.set_y(new_head_y)
        self.__last_direction = direction

        # Additional reward for staying alive or growing
        if not self.__is_dead:
            reward += settings.TIME_ALIVE_REWARD
            reward += settings.SIZE_REWARD_MULTIPLIER * self.get_size()

        return reward

    def eat(self, apple: Apple) -> int:
        """
        Handles the snake eating an apple.
        The snake grows if the apple is green, otherwise, it loses a segment.
        If the snake's length drops to 0, the game ends.

        :param apple: The apple that the snake is eating.
        :type apple: Apple
        :raises GameOver: If the snake's length drops to 0.
        :return: The reward associated with eating the apple.
        :rtype: int
        """
        initial_reward = apple.get_reward()
        total_reward = initial_reward

        if apple.is_green():
            # Green apple: snake's length increase by 1.
            total_reward += settings.GREEN_APPLE_BONUS
            
            x, y = self.__last_direction.value

            if len(self.__body) > 0:
                last_body = self.__body[-1]
            else:
                last_body = self.get_position()

            # Grow the snake by adding a new body segment
            self.__body.append((last_body[0] + x, last_body[1] + y))
        else:
            # Red apple: snake's length decrease by 1.a
            if self.get_size() - 1 == 0:
                # If no body segments left after eating red apple, game over
                self.__is_dead = True
                raise GameOver("Snake length dropped to 0. Game over!")

            self.__body.pop()  # Remove last body segment
            total_reward += settings.RED_APPLE_PENALTY

        # New apple appears on the board after consumption
        self.__world.remove_entity(apple)
        self.__world.spawn_entity(apple)

        # Bonus rewards based on snake size (example, adjust as needed)
        if total_reward > 0 and self.get_size() >= settings.TARGET_LENGTH:
            total_reward += settings.TARGET_LENGTH_BONUS
        elif total_reward > 0 and self.get_size() % 5 == 0:
            total_reward += settings.SIZE_MILESTONE_BONUS

        return total_reward

    def get_state_at_relative_pos(self, dx: int, dy: int) -> str:
        """
        Returns the character representation of the element at a relative
        position (dx, dy) from the snake's head.

        Used to determine what the snake "sees" in its immediate vicinity.

        :param dx: Relative X-coordinate from the snake's head.
        :type dx: int
        :param dy: Relative Y-coordinate from the snake's head.
        :type dy: int
        :return: A character representing the state of the position.
        :rtype: str
        """
        x, y = self.get_x() + dx, self.get_y() + dy

        # Check if out of bounds first, as it implies a wall

        if not self.__world.is_within_bounds(x, y):
            return settings.WALL_CHAR

        # Check for snake body collision

        if (x, y) in self.__body:
            return settings.SNAKE_SEGMENT_CHAR

        # Check for entities
        entity_at_pos = self.__world.get_location(x, y).get_entity()
        if isinstance(entity_at_pos, Apple):
            if entity_at_pos.is_green():
                return settings.GREEN_APPLE_CHAR
            return settings.RED_APPLE_CHAR

        # Empty space
        return settings.EMPTY_CHAR

    def get_state(self) -> list[bool]:
        """
        Returns a boolean list representing the game state from the snake's
        perspective. This state is passed to the AI agent.

        The agent can only see in the 4 directions from its head.
        Providing more information will result in a penalty.

        The returned list contains information about obstacles (walls or body)
        and apples in each of the four cardinal directions (UP, DOWN, LEFT, RIGHT).
        The order of elements in the list is:
        [obstacle_up, obstacle_down, obstacle_left, obstacle_right,
         green_apple_up, green_apple_down, green_apple_left, green_apple_right,
         red_apple_up, red_apple_down, red_apple_left, red_apple_right]

        :return: The encoded state of the environment for the agent.
        :rtype: list[bool]
        """
        state = [False] * 12  # Initialize all to False

        head_x, head_y = self.get_x(), self.get_y()

        # Define directions and corresponding state indices
        directions_info = {
            Direction.UP: (0, -1, 0),    # obstacle_up, green_up, red_up
            Direction.DOWN: (0, 1, 1),   # obstacle_down, green_down, red_down
            Direction.LEFT: (-1, 0, 2),  # obstacle_left, green_left, red_left
            Direction.RIGHT: (1, 0, 3),  # obstacle_right, green_right, red_right
        }

        for direction, (dx, dy, idx_offset) in directions_info.items():
            current_x, current_y = head_x + dx, head_y + dy
           
            while self.__world.is_within_bounds(current_x, current_y):
                char = self.get_state_at_relative_pos(
                    current_x - head_x, current_y - head_y
                )

                if char == settings.WALL_CHAR or char == settings.SNAKE_SEGMENT_CHAR:
                    state[idx_offset] = True  # Obstacle detected
                    break
                elif char == settings.GREEN_APPLE_CHAR:
                    state[idx_offset + 4] = True  # Green apple detected
                    break
                elif char == settings.RED_APPLE_CHAR:
                    state[idx_offset + 8] = True  # Red apple detected
                    break
               
                # Move to the next cell in this direction
                current_x += dx
                current_y += dy
            else:
                if not self.__world.is_within_bounds(current_x, current_y):
                     state[idx_offset] = True # Indicate wall at edge if not already set.

        return state

    def get_body(self) -> deque[tuple[int, int]]:
        """
        Returns the deque of body segments of the snake.

        :return: The body segments of the snake as a deque of (x, y) tuples.
        :rtype: deque[tuple[int, int]]
        """
        return self.__body

    def set_body(self, body: list[tuple[int, int]]) -> None:
        """
        Sets the snake's body to the specified sequence of positions.
        This is useful for loading game states or for specific testing.

        :param body: A list of (x, y) coordinates representing the new body
                     segments of the snake, where the first element is the head.
        :type body: list[tuple[int, int]]
        """
        self.__body = deque(body)

    def get_size(self) -> int:
        """
        Returns the current size of the snake.

        The size is calculated as 1 (for the snake's head) plus the length of
        its body segments.

        :return: The total number of segments composing the snake
                 (head + body).
        :rtype: int
        """
        return 1 + len(self.__body)

    def contains_point(self, x: int, y: int) -> bool:
        """
        Checks whether the point (x, y) is occupied by the snake (head or body).

        :param x: The X coordinate to check.
        :type x: int
        :param y: The Y coordinate to check.
        :type y: int
        :return: True if the point (x, y) is within the snake's head position
                 or is one of its body segments, False otherwise.
        :rtype: bool
        """
        return super().contains_point(x, y) or (x, y) in self.get_body()

    def get_char(self) -> str:
        """
        Returns the character representation of the snake's head, colored for
        terminal output.

        :return: A string representing the snake's head, colored in yellow.
        :rtype: str
        """
        return f"\033[33m{settings.SNAKE_HEAD_CHAR}\033[0m"

    def get_last_direction(self) -> Direction:
        """
        Returns the last direction the snake moved.

        :return: The last movement direction.
        :rtype: Direction
        """
        return self.__last_direction

    def is_dead(self) -> bool:
        """
        Checks if the snake is currently dead.

        :return: True if the snake is dead, False otherwise.
        :rtype: bool
        """
        return self.__is_dead

    def render(self) -> list[tuple[str, int, int]]:
        """
        Generates a list of (character, x, y) tuples for rendering the snake
        (head and body) on the board.

        :return: A list containing tuples with:
                 - the character to display,
                 - the X coordinate,
                 - the Y coordinate.
        :rtype: list[tuple[str, int, int]]
        """
        # Render head first
        render_list = super().render()

        # Render body segments
        for body_segment_x, body_segment_y in self.__body:
            render_list.append(
                (settings.SNAKE_SEGMENT_CHAR, body_segment_x, body_segment_y)
            )

        return render_list