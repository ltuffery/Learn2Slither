import pytest

from engine.world import World
from engine.entity.snake import Snake
import engine.settings as engine_settings
from engine.entity.apple import Apple, AppleType
from collections import deque
from abc import ABC, abstractmethod # Pour vérifier si Entity est abstraite


# --- Ajout d'une DummyEntity si votre Entity est abstraite ---
# Pour éviter les problèmes d'importation circulaire ou si Entity est abstraite,
# vous pouvez créer une petite classe concrète pour les tests.
# Vérifiez si votre 'Entity' de 'engine' est déjà abstraite.
# Si 'Entity' de 'engine' n'est PAS abstraite et a déjà un __init__ simple,
# vous pouvez retirer ce bloc DummyEntity et utiliser directement 'Entity()'
# en vous assurant qu'elle n'a pas de paramètres obligatoires.
# Sinon, cette DummyEntity est nécessaire.

# Vérifions si la classe Entity importée est abstraite.
# C'est un peu "hacky" mais utile pour le contexte de test.
# Normalement, vous sauriez si votre Entity est abstraite.
try:
    if issubclass(Entity, ABC):
        class ConcreteTestEntity(Entity):
            def __init__(self, x: int = 0, y: int = 0):
                # Assurez-vous d'appeler le constructeur parent si nécessaire
                super().__init__(x=x, y=y) # ou super().__init__() si pas de x,y
            def get_char(self) -> str:
                return "T" # Un caractère de test
            def render(self) -> list[tuple[str, int, int]]:
                return [(self.get_char(), self._x, self._y)]
            # Implémentez toutes les autres méthodes abstraites si Entity en a d'autres
        TestEntity = ConcreteTestEntity
    else:
        # Si Entity n'est pas abstraite, on peut l'utiliser directement si son __init__ est simple.
        # Si son __init__ a des paramètres, vous devrez peut-être en faire une ConcreteTestEntity
        # même si elle n'est pas abstraite.
        TestEntity = Entity
except NameError:
    # Si Entity n'est pas définie du tout (pb d'import), on définit une base minimale
    class TestEntity(ABC): # Définir une base simple si 'engine.entity.entity.Entity' n'est pas accessible
        def __init__(self, x: int = 0, y: int = 0):
            self._x = x
            self._y = y
        def get_x(self): return self._x
        def get_y(self): return self._y
        def teleport(self, x, y): self._x, self._y = x, y
        def contains_point(self, x, y): return self._x == x and self._y == y
        @abstractmethod
        def get_char(self): return 'E'
        @abstractmethod
        def render(self): return [(self.get_char(), self._x, self._y)]

    class ConcreteTestEntity(TestEntity):
        def get_char(self) -> str:
            return "T"
        def render(self) -> list[tuple[str, int, int]]:
            return [(self.get_char(), self._x, self._y)]
    TestEntity = ConcreteTestEntity


# --- Fixtures pour le World (inchangées) ---

@pytest.fixture
def world_instance():
    original_height = engine_settings.HEIGHT
    original_width = engine_settings.WIDTH
    engine_settings.HEIGHT = 20
    engine_settings.WIDTH = 20
    world = World()
    yield world
    engine_settings.HEIGHT = original_height
    engine_settings.WIDTH = original_width


@pytest.fixture
def empty_world(world_instance):
    world_instance._World__entities = []
    return world_instance

@pytest.fixture
def world_with_entities(world_instance):
    world_instance._World__entities = []

    snake = Snake(world_instance)
    snake.teleport(world_instance.get_width() // 2, world_instance.get_height() // 2)
    world_instance.add_entity(snake)

    empty_locs = world_instance.get_empty_locations()
    if len(empty_locs) >= 2:
        pos1 = empty_locs[0]
        pos2 = empty_locs[1]
    else:
        pos1 = (1, 1)
        pos2 = (1, 2)


    apple1 = Apple(world_instance, AppleType.GREEN)
    apple1.teleport(pos1[0], pos1[1])
    world_instance.add_entity(apple1)

    apple2 = Apple(world_instance, AppleType.RED)
    apple2.teleport(pos2[0], pos2[1])
    world_instance.add_entity(apple2)

    return world_instance

# --- Fixtures pour les Entités (inchangées, utilisent TestEntity pour Apple) ---

@pytest.fixture
def snake(world_instance):
    """Fournit une instance de serpent de taille minimale dans un monde."""
    s = Snake(world_instance)
    # Assurez-vous que le serpent est bien initialisé (teleporté et de taille initiale)
    s.teleport(world_instance.get_width() // 2, world_instance.get_height() // 2)
    return s

@pytest.fixture
def long_snake(world_instance):
    """Fournit une instance de serpent plus longue pour tester le mouvement.
    La position est gérée par l'initialiseur du Snake."""
    s = Snake(world_instance)
    # Ajout au monde
    world_instance.add_entity(s)
    # Faites grandir le serpent pour qu'il ait plus de segments
    # En ajoutant simplement de nouveaux segments à son corps (simule la croissance)
    # Note: Cela ne simule pas un "vrai" grow() via Apple, juste l'augmentation de taille.
    head_x, head_y = s.get_position()
    last_body_x, last_body_y = s.get_body()[-1] if s.get_body() else (head_x, head_y)
    
    # Pour allonger le serpent, nous ajoutons des segments en 'arrière' de sa queue.
    # On simule un mouvement vers l'avant pour que les nouveaux segments soient derrière.
    dx, dy = s.get_last_direction().value
    # On ajoute dans la direction opposée pour que les nouveaux segments soient bien la queue
    for i in range(1, 6): # Ajouter 5 segments
        new_segment_x = head_x - dx * i
        new_segment_y = head_y - dy * i
        # Simple ajout, on ne se préoccupe pas des collisions ici, c'est pour un état de test.
        # Si vous avez une vraie méthode `grow` qui ajoute des segments, utilisez-la.
        s._Snake__body.append((new_segment_x, new_segment_y))
    
    return s

@pytest.fixture
def green_apple(world_instance):
    return Apple(world_instance, AppleType.GREEN)

@pytest.fixture
def red_apple(world_instance):
    return Apple(world_instance, AppleType.RED)