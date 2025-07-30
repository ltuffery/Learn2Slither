from engine.world import World
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType


from tests.conftest import TestEntity # Importer la TestEntity définie dans conftest


# --- Benchmarks pour la classe World ---

def test_world_init_benchmark(benchmark):
    """Benchmark de la méthode __init__ de la classe World."""
    benchmark(World)

def test_world_get_width_benchmark(benchmark, world_instance):
    """Benchmark de la méthode get_width."""
    benchmark(world_instance.get_width)

def test_world_get_height_benchmark(benchmark, world_instance):
    """Benchmark de la méthode get_height."""
    benchmark(world_instance.get_height)

def test_world_get_location_empty_benchmark(benchmark, empty_world):
    """Benchmark de get_location pour une case vide."""
    x, y = empty_world.get_width() // 2, empty_world.get_height() // 2
    benchmark(empty_world.get_location, x, y)

def test_world_get_location_wall_benchmark(benchmark, empty_world):
    """Benchmark de get_location pour un mur."""
    benchmark(empty_world.get_location, 0, 0)

def test_world_get_location_with_entity_benchmark(benchmark, world_with_entities):
    """Benchmark de get_location pour une case avec entité (serpent)."""
    snake = world_with_entities.get_entities()[0]
    x, y = snake.get_x(), snake.get_y()
    benchmark(world_with_entities.get_location, x, y)

def test_world_get_empty_locations_benchmark(benchmark, world_instance):
    """Benchmark de get_empty_locations dans un monde presque vide."""
    def setup_empty_locations():
        world_instance._World__entities = []
        snake_for_setup = Snake(world_instance)
        snake_for_setup.teleport(world_instance.get_width() // 2, world_instance.get_height() // 2)
        world_instance.add_entity(snake_for_setup)
        # Ne retourne rien, prépare juste l'état
        pass

    benchmark.pedantic(world_instance.get_empty_locations, setup=setup_empty_locations, rounds=100)


def test_world_get_entity_at_empty_benchmark(benchmark, empty_world):
    """Benchmark de get_entity_at pour une case vide."""
    x, y = empty_world.get_width() // 2, empty_world.get_height() // 2
    benchmark(empty_world.get_entity_at, x, y)

def test_world_get_entity_at_with_entity_benchmark(benchmark, world_with_entities):
    """Benchmark de get_entity_at pour une case avec entité."""
    snake = world_with_entities.get_entities()[0]
    x, y = snake.get_x(), snake.get_y()
    benchmark(world_with_entities.get_entity_at, x, y)

def test_world_get_entities_benchmark(benchmark, world_with_entities):
    """Benchmark de la méthode get_entities."""
    benchmark(world_with_entities.get_entities)

def test_world_add_entity_benchmark(benchmark, empty_world):
    """Benchmark de la méthode add_entity."""
    def setup_add_entity():
        empty_world._World__entities = []
        temp_entity = TestEntity(x=1, y=1)
        return (temp_entity,), {}

    benchmark.pedantic(empty_world.add_entity, setup=setup_add_entity, rounds=1000)

def test_world_spawn_entity_benchmark(benchmark, empty_world):
    """Benchmark de la méthode spawn_entity."""
    def setup_spawn_entity():
        empty_world._World__entities = []
        apple_to_spawn = Apple(empty_world, AppleType.GREEN)
        # Retourne la pomme dans un tuple
        return (apple_to_spawn,), {}

    benchmark.pedantic(empty_world.spawn_entity, setup=setup_spawn_entity, rounds=100)

def test_world_remove_entity_benchmark(benchmark, world_with_entities):
    """Benchmark de la méthode remove_entity."""
    def setup_remove_entity():
        temp_apple = Apple(world_with_entities, AppleType.GREEN)
        temp_apple.teleport(1, 1)
        world_with_entities.add_entity(temp_apple)
        return (temp_apple,), {}

    benchmark.pedantic(world_with_entities.remove_entity, setup=setup_remove_entity, rounds=1000)

def test_world_render_benchmark(benchmark, world_with_entities):
    """Benchmark de la méthode render."""
    benchmark(world_with_entities.render)
