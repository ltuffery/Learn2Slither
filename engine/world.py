import copy
import random
import sys

import engine.settings as settings
from engine.entity.entity import Entity
# from engine.entity.snake import Snake  # Import Snake to use in render
from engine.map_location import MapLocation


class World:
    """
    Represents the game world, containing a grid-based map and game entities.

    The world manages the placement and interaction of entities within its
    boundaries, providing information about specific locations.

    :ivar __world_grid: The 2D grid representing the game map, including walls.
    :vartype __world_grid: list[list[str]]
    :ivar __height: The height of the playable area of the world (excluding walls).
    :vartype __height: int
    :ivar __width: The width of the playable area of the world (excluding walls).
    :vartype __width: int
    :ivar __entities: A list of all entities currently present in the world.
    :vartype __entities: list[Entity]
    """

    def __init__(self):
        """
        Initializes the game world with dimensions specified in settings.
        The world grid includes a border of walls.
        """
        if settings.HEIGHT < 1 or settings.WIDTH < 1:
            raise ValueError("Height and width must be at least 1 for "
                             "playable area.")

        self.__height: int = settings.HEIGHT
        self.__width: int = settings.WIDTH
        self.__world_grid: list[list[str]] = []
        self.__entities: list[Entity] = []

        self._make_world_grid()

    def _make_world_grid(self) -> None:
        """
        Generates the internal 2D grid representation of the world,
        including walls around the edges.
        The playable area is `self.__height` by `self.__width`.
        The total grid size is `(self.__height + 2)` by `(self.__width + 2)`.
        """
        # Top wall
        self.__world_grid.append([settings.WALL_CHAR] * (self.__width + 2))

        # Middle rows (playable area + side walls)
        for _ in range(self.__height):
            row: list[str] = [settings.WALL_CHAR]
            row.extend([settings.EMPTY_CHAR] * self.__width)
            row.append(settings.WALL_CHAR)
            self.__world_grid.append(row)

        # Bottom wall
        self.__world_grid.append([settings.WALL_CHAR] * (self.__width + 2))

    def get_width(self) -> int:
        """
        Returns the width of the playable area of the world.

        :return: The width of the playable area.
        :rtype: int
        """
        return self.__width

    def get_height(self) -> int:
        """
        Returns the height of the playable area of the world.

        :return: The height of the playable area.
        :rtype: int
        """
        return self.__height

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Checks if the given coordinates are within the *total grid* bounds,
        including the wall boundaries.

        :param x: The X-coordinate to check.
        :type x: int
        :param y: The Y-coordinate to check.
        :type y: int
        :return: True if coordinates are within the grid, False otherwise.
        :rtype: bool
        """
        # Check against total grid dimensions (including walls)
        return (
            0 <= y < (self.__height + 2) and
            0 <= x < (self.__width + 2)
        )

    def get_location(self, x: int, y: int) -> MapLocation:
        """
        Retrieves a `MapLocation` object representing the specified position
        in the world grid. Handles out-of-bounds coordinates by treating them
        as walls.

        :param x: The X-coordinate.
        :type x: int
        :param y: The Y-coordinate.
        :type y: int
        :return: A MapLocation object representing the position's state.
        :rtype: MapLocation
        """
        if not self.is_within_bounds(x, y):
            # Treat out-of-bounds as walls
            return MapLocation(x, y, is_wall=True, entity=None)

        # Determine if it's a structural wall (from __world_grid)
        is_structural_wall = (
            self.__world_grid[y][x] == settings.WALL_CHAR
        )

        # Check for entity at this location
        entity_at_pos = self.get_entity_at(x, y)

        # A location is a "wall" if it's a structural wall or occupied by a snake body
        # For simplicity, MapLocation considers is_wall true only for structural walls
        # Collision logic with snake body is handled by Snake itself.
        return MapLocation(x, y, is_structural_wall, entity_at_pos)

    def get_empty_locations(self) -> list[tuple[int, int]]:
        """
        Retrieves a list of all empty, non-wall locations in the playable area
        of the world.

        An "empty" location is one that is not occupied by a wall and does not
        contain any entity.

        :return: A list of coordinates (x, y) where there are no entities
                 and no structural walls.
        :rtype: list[tuple[int, int]]
        """
        empty_list = []

        for y in range(1, self.__height + 1):
            for x in range(1, self.__width + 1):
                if self.__world_grid[y][x] == settings.EMPTY_CHAR:
                    if self.get_entity_at(x, y) is None:
                        empty_list.append((x, y))
        return empty_list

    def get_entity_at(self, x: int, y: int) -> Entity | None:
        """
        Retrieves an entity at the given coordinates.
        This checks if any entity's area (`contains_point`) includes (x, y).

        :param x: The X-coordinate.
        :type x: int
        :param y: The Y-coordinate.
        :type y: int
        :return: The entity found at the coordinates, or None if no entity
                 occupies that space.
        :rtype: Entity | None
        """
        for entity in self.__entities:
            if entity.contains_point(x, y):
                return entity
        return None

    def get_entities(self) -> list[Entity]:
        """
        Returns the list of all entities currently present in the world.

        :return: A list containing all entities in the world.
        :rtype: list[Entity]
        """
        return self.__entities

    def add_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the world's internal list of entities.
        This does not handle entity placement (teleporting).

        :param entity: The entity to be added to the world.
        :type entity: Entity
        """
        self.__entities.append(entity)

    def spawn_entity(self, entity: Entity) -> None:
        """
        Spawns an entity into the world by placing it at a random
        empty location and adding it to the world's entities.

        :param entity: The entity to spawn.
        :type entity: Entity
        :raises ValueError: If no empty locations are available.
        """
        empty_locations = self.get_empty_locations()
        if not empty_locations:
            raise ValueError("No empty locations available to spawn entity.")

        x, y = random.choice(empty_locations)
        entity.teleport(x, y)
        self.add_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        """
        Removes an entity from the world.

        :param entity: The entity to remove.
        :type entity: Entity
        """
        if entity in self.__entities:
            self.__entities.remove(entity)

    def render(self, title: str = None) -> None:
        """
        Renders the current state of the world to the terminal.
        This includes the world grid with walls, entities (snake and apples),
        and the snake's last direction.

        Important: This method prints the full board and the snake's
        last direction. It does NOT print the snake's `get_state()` output
        (the vision), as that is for the AI agent's internal use and
        should be handled separately as per the subject requirements for
        terminal output (which implies a visual grid and separate AI info).

        :param title: An optional title to display above the rendered world.
        :type title: str, optional
        """
        from engine.entity.snake import Snake

        sys.stdout.write("\033[H")  # Moves cursor to the top-left
        sys.stdout.write("\033[J")  # Clears the terminal

        # Create a deep copy of the base world grid for rendering purposes
        # This allows us to place entity characters without modifying
        # the underlying structural grid.
        display_grid = copy.deepcopy(self.__world_grid)

        # Place entities onto the display grid
        for entity in self.__entities:
            for char, x, y in entity.render():
                if self.is_within_bounds(x, y):
                    display_grid[y][x] = char

        # Find the snake to display its last direction
        snake_instance: Snake | None = None
        for entity in self.__entities:
            if isinstance(entity, Snake):
                snake_instance = entity
                break

        if title is not None:
            print(title + "\n\n")

        # Print the board and snake's last direction
        for row_idx, row_chars in enumerate(display_grid):
            # If it's the row where the snake's head is (assuming single snake)
            # Or if it's the row right below the board for direction display
            if snake_instance and row_idx == snake_instance.get_y():
                print("".join(row_chars) + f"   Direction: {snake_instance.get_last_direction().name}")
            else:
                print("".join(row_chars))

        sys.stdout.flush()