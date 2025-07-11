from engine.map_location import MapLocation
from engine.entity.entity import Entity
import sys
import copy
import random
import engine.settings as settings


class World:
    """
    Represents the game world, containing a grid-based map and game entities.

    Attributes:
        __world (list[list[str]]): The 2D grid representing the game map.
        __height (int): The height of the world (number of rows).
        __width (int): The width of the world (number of columns).
        __entities (list[Entity]): A list of all entities present in the world.
    """

    def __init__(self):
        """
        Initializes the game world with a specified height and width.

        Args:
            height (int, optional): The height of the world. Defaults to 10.
            width (int, optional): The width of the world. Defaults to 10.
        """
        if settings.HEIGHT < 3 or settings.WIDTH < 3:
            raise ValueError("Height and width must be >= 3")

        self.__world: list[list[str]] = []
        self.__height: int = settings.HEIGHT
        self.__width: int = settings.WIDTH
        self.__entities: list[Entity] = []

        self.__make_world()

    def __make_world(self) -> None:
        """
        Generates the world grid, adding walls around the edges.
        """
        for i in range(self.__height + 2):
            if i == 0 or i == self.__height + 1:
                self.__world.append(['*' for _ in range(self.__width + 2)])
                continue

            row: list = ['*']

            for _ in range(self.__width):
                row.append(' ')

            row.append('*')
            self.__world.append(row)

    def get_width(self) -> int:
        """
        Returns the width of the object.

        Returns:
            int: The width of the object.
        """
        return self.__width

    def get_height(self) -> int:
        """
        Returns the height of the object.

        Returns:
            int: The height of the object.
        """
        return self.__height

    def get_location(self, x: int, y: int) -> MapLocation:
        """
        Retrieves a `MapLocation` object representing a given position.

        Args:
            x (int): The X-coordinate.
            y (int): The Y-coordinate.

        Returns:
            MapLocation: The location object representing the position.

        Raises:
            Exception: If the provided coordinates are out of bounds.
        """
        if y > len(self.__world) or x > len(self.__world[y]):
            raise Exception('Invalid location')

        is_wall = self.__world[y][x] == '*'

        return MapLocation(x, y, is_wall, self.get_entity_at(x, y))

    def get_empty_locations(self) -> list[tuple[int, int]]:
        """
        Retrieves a list of all empty locations in the world.

        Returns:
            list[tuple[int, int]]: A list of coordinates (x, y) where there
            are no entities.
        """
        empty_list = []

        for y in range(len(self.__world)):
            for x in range(len(self.__world[y])):
                ceil = self.__world[y][x]

                if ceil != ' ':
                    continue

                if self.get_entity_at(x, y) is None:
                    empty_list.append((x, y))

        return empty_list

    def get_entity_at(self, x: int, y: int) -> Entity | None:
        """
        Retrieves an entity at the given coordinates.

        Args:
            x (int): The X-coordinate.
            y (int): The Y-coordinate.

        Returns:
            object | None: The entity found at the coordinates, or None if
            empty.
        """
        for entity in self.__entities:
            if entity.contains_point(x, y):
                return entity
        return None

    def get_entities(self) -> list[Entity]:
        """
        Returns the list of all entities currently present in the world.

        Returns:
            list[Entity]: A list containing all entities in the world.
        """
        return self.__entities

    def add_entity(self, entity: Entity):
        """
        Adds an entity to the world.

        Args:
            entity (Entity): The entity to be added to the world.
        """
        self.__entities.append(entity)

    def spawn_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the world.

        Args:
            entity (object): The entity to add.
        """
        x, y = random.choice(self.get_empty_locations())

        entity.teleport(x, y)

        self.add_entity(entity)

    def remove_entity(self, entity: Entity):
        """
        Removes an entity from the world.

        Args:
            entity (Entity): The entity to remove.
        """
        self.__entities.remove(entity)

    def render(self, title: str = None):
        """
        Renders the current state of the world to the terminal.
        """
        from engine.entity.snake import Snake

        sys.stdout.write("\033[H")  # Moves cursor to the top-left
        sys.stdout.write("\033[J")  # Clears the terminal

        world = copy.deepcopy(self.__world)

        for entity in self.__entities:
            for position in entity.render():
                world[position[2]][position[1]] = position[0]

        snake = [e for e in self.__entities if isinstance(e, Snake)][0]

        if title is not None:
            print(title + "\n\n")

        def str_see(it):
            return ' ' if it is None else it

        print(snake.get_last_direction().name)
        for i in range(len(world)):
            snake_see = "".join(
                str_see(item) for item in snake.see()[i]
            )
            print("".join(world[i]) + "   " + snake_see)

        sys.stdout.flush()
