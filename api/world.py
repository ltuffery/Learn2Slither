from api.map_location import MapLocation
import sys
import copy


class World:
    def __init__(self, heigth=10, width=10):
        self.__world: list = []
        self.__heigth: int = heigth
        self.__width: int = width
        self.__entities: list = []

        self.__make_world()

    def __make_world(self) -> None:
        for i in range(self.__heigth + 2):
            if i == 0 or i == self.__heigth + 1:
                self.__world.append(['*' for _ in range(self.__width + 2)])
                continue

            ceil: list = ['*']

            for _ in range(self.__width):
                ceil.append(' ')

            ceil.append('*')
            self.__world.append(ceil)

    def get_location(self, x: int, y: int) -> MapLocation:
        if y > len(self.__world) or x > len(self.__world[y]):
            raise Exception('Invalid location')

        if self.get_entity_at(x, y) is None:
            return MapLocation(x, y, self.__world[y][x] == ' ')

        return MapLocation(x, y, False)

    def get_entity_at(self, x: int, y: int):
        for entity in self.__entities:
            if entity.get_x() == x and entity.get_y() == y:
                return entity
        return None

    def spaw_entity(self, entity) -> None:
        self.__entities.append(entity)

    def render(self):
        sys.stdout.write("\033[H")
        sys.stdout.write("\033[J")

        world = copy.deepcopy(self.__world)

        for _, entity in enumerate(self.__entities):
            world[entity.get_y()][entity.get_x()] = '#'

            # for _, body in enumerate(entity.get_body()):
            #     world[body.get_y()][body.get_x()] = 'T'

        for _, line in enumerate(world):
            print("".join(line))

        sys.stdout.flush()
