import unittest
from engine.entity.snake import Snake
from api.direction import Direction
from engine.world import World


class TestSnake(unittest.TestCase):
    def setUp(self):
        world = World()
        self.snake = Snake(world, 5, 5, Direction.SUD)

        return super().setUp()

    def test_get_x(self):
        self.assertEqual(5, self.snake.get_x())

    def test_get_y(self):
        self.assertEqual(5, self.snake.get_y())

    def test_move(self):
        for direction in list(Direction):
            with self.subTest(direction):
                world = World()
                snake = Snake(world, 5, 5, direction.opposite())
                x = snake.get_x()
                y = snake.get_y()

                snake.move(direction)

                self.assertEqual(x + direction.value[0], snake.get_x())
                self.assertEqual(y + direction.value[1], snake.get_y())


if __name__ == '__main__':
    unittest.main()
