import pytest

from engine.direction import Direction
from engine.entity.apple import Apple, AppleType
from engine.entity.snake import Snake
from engine.world import World


@pytest.mark.benchmark(group="snake")
def test_something(benchmark):
    world = World()
    snake = Snake(world)
    apple = Apple(world, AppleType.GREEN)

    world.spawn_entity(snake)
    world.spawn_entity(apple)

    benchmark(snake.eat, apple)

    assert True
