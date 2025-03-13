from api.map_location import MapLocation
import sys
import copy


class World:
    """
    Represents the game world, containing a grid-based map and game entities.

    Attributes:
        __world (list[list[str]]): The 2D grid representing the game map.
        __height (int): The height of the world (number of rows).
        __width (int): The width of the world (number of columns).
        __entities (list): A list of all entities present in the world.
    """

    def __init__(self, height=10, width=10):
        """
        Initializes the game world with a specified height and width.

        Args:
            height (int, optional): The height of the world. Defaults to 10.
            width (int, optional): The width of the world. Defaults to 10.
        """
        self.__world: list = []
        self.__height: int = height
        self.__width: int = width
        self.__entities: list = []

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

        if self.get_entity_at(x, y) is None:
            return MapLocation(x, y, self.__world[y][x] == ' ')

        return MapLocation(x, y, False)

    def get_entity_at(self, x: int, y: int):
        """
        Retrieves an entity at the given coordinates.

        Args:
            x (int): The X-coordinate.
            y (int): The Y-coordinate.

        Returns:
            object | None: The entity found at the coordinates, or None if empty.
        """
        for entity in self.__entities:
            if entity.get_x() == x and entity.get_y() == y:
                return entity
        return None

    def spawn_entity(self, entity) -> None:
        """
        Adds an entity to the world.

        Args:
            entity (object): The entity to add.
        """
        self.__entities.append(entity)

    def render(self):
        """
        Renders the current state of the world to the terminal.
        """
        sys.stdout.write("\033[H")  # Moves cursor to the top-left
        sys.stdout.write("\033[J")  # Clears the terminal

        world = copy.deepcopy(self.__world)

        for entity in self.__entities:
            world[entity.get_y()][entity.get_x()] = '#'

            # Uncomment if you want to render the snake's body
            # for body in entity.get_body():
            #     world[body.get_y()][body.get_x()] = 'T'

        for line in world:
            print("".join(line))

        sys.stdout.flush()
