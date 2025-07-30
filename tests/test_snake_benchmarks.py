import random
from engine.direction import Direction
from engine.entity.snake import Snake
from engine.entity.apple import Apple, AppleType


def test_snake_init_benchmark(benchmark, world_instance):
    """Benchmark de l'initialisation du serpent."""
    # La fixture snake s'occupe de l'ajout au monde pour des tests cohérents
    benchmark(Snake, world_instance)

def test_snake_get_length_benchmark(benchmark, snake):
    """Benchmark de la récupération de la longueur du serpent (via get_size)."""
    benchmark(snake.get_size) # Votre méthode est get_size

def test_snake_get_head_benchmark(benchmark, snake):
    """Benchmark de la récupération de la tête du serpent (via get_position)."""
    benchmark(snake.get_position) # Votre méthode est get_position

def test_snake_get_last_direction_benchmark(benchmark, snake):
    """Benchmark de la récupération de la dernière direction du serpent."""
    benchmark(snake.get_last_direction)

def test_snake_teleport_benchmark(benchmark, snake):
    """Benchmark de la téléportation du serpent."""
    def setup_teleport():
        # Générer de nouvelles coordonnées valides pour éviter les murs/corps
        world_width = snake._Snake__world.get_width()
        world_height = snake._Snake__world.get_height()
        
        # Trouver un emplacement vide pour la téléportation
        empty_locs = snake._Snake__world.get_empty_locations()
        # Filtrer les emplacements qui ne sont pas occupés par le corps du serpent actuel
        safe_empty_locs = [loc for loc in empty_locs if loc not in snake.get_body() and loc != snake.get_position()]

        if not safe_empty_locs:
            # Fallback si aucun emplacement vide sûr, ce qui est peu probable pour 20x20
            # Pour un benchmark, c'est mieux de s'assurer d'un succès
            new_x = world_width // 2
            new_y = world_height // 2
        else:
            new_x, new_y = random.choice(safe_empty_locs) # Utilisation de random standard ici

        return (new_x, new_y), {}
    
    # La méthode teleport de votre Snake contient des boucles aléatoires.
    # C'est une opération plus complexe à benchmarker.
    benchmark.pedantic(snake.teleport, setup=setup_teleport, rounds=100) # Moins de rounds car coûteux

def test_snake_move_benchmark(benchmark, snake):
    """Benchmark du mouvement du serpent dans un monde vide (sans collision)."""
    def setup_move():
        world = snake._Snake__world
        # Assurez-vous que le monde est configuré pour un mouvement simple
        # sans collision imminente pour le benchmark.
        world._World__entities = [snake] # Seul le serpent est dans le monde
        
        # Téléporter le serpent à un endroit sûr et orienté vers un espace vide
        safe_x, safe_y = world.get_width() // 2, world.get_height() // 2
        snake.teleport(safe_x, safe_y)
        
        # S'assurer que la prochaine case est vide pour un mouvement normal
        # et définir une direction si ce n'est pas déjà le cas dans teleport
        next_x, next_y = safe_x + snake.get_last_direction().value[0], safe_y + snake.get_last_direction().value[1]
        
        # Empêcher une collision auto-générée si le corps est initialisé de manière complexe
        # Si le snake.__init__ met déjà le serpent à une position valide,
        # et que le corps suit, il suffit de s'assurer que la prochaine case est libre.
        if world.get_location(next_x, next_y).is_wall() or (next_x, next_y) in snake.get_body():
            # Si la direction actuelle mène à un mur ou au corps, essayez une autre direction
            for d in list(Direction):
                temp_next_x = safe_x + d.value[0]
                temp_next_y = safe_y + d.value[1]
                if not world.get_location(temp_next_x, temp_next_y).is_wall() and \
                   (temp_next_x, temp_next_y) not in snake.get_body():
                    snake._Snake__last_direction = d # Changer la direction pour le test
                    break
        
        # Le move prend une direction en argument, nous devons la fournir
        # On va choisir la direction actuelle du serpent après le teleport.
        direction_for_move = snake.get_last_direction()
        return (direction_for_move,), {}
    
    benchmark.pedantic(snake.move, setup=setup_move, rounds=1000)

def test_snake_move_long_snake_benchmark(benchmark, long_snake):
    """Benchmark du mouvement d'un long serpent."""
    def setup_move_long():
        world = long_snake._Snake__world
        world._World__entities = [long_snake]
        
        # Téléporter le serpent pour qu'il ne se heurte pas immédiatement
        safe_x, safe_y = world.get_width() // 2, world.get_height() // 2
        long_snake.teleport(safe_x, safe_y)
        
        # Assurer une direction de mouvement valide
        next_x, next_y = safe_x + long_snake.get_last_direction().value[0], safe_y + long_snake.get_last_direction().value[1]
        if world.get_location(next_x, next_y).is_wall() or (next_x, next_y) in long_snake.get_body():
            for d in list(Direction):
                temp_next_x = safe_x + d.value[0]
                temp_next_y = safe_y + d.value[1]
                if not world.get_location(temp_next_x, temp_next_y).is_wall() and \
                   (temp_next_x, temp_next_y) not in long_snake.get_body():
                    long_snake._Snake__last_direction = d
                    break
                    
        direction_for_move = long_snake.get_last_direction()
        return (direction_for_move,), {}
    
    benchmark.pedantic(long_snake.move, setup=setup_move_long, rounds=1000)


def test_snake_eat_green_apple_benchmark(benchmark, snake, green_apple):
    """Benchmark de la consommation d'une pomme verte (implique croissance)."""
    def setup_eat_green():
        world = snake._Snake__world
        world._World__entities = [] # Vider les entités
        
        # Positionner le serpent
        snake_x, snake_y = world.get_width() // 2, world.get_height() // 2
        snake.teleport(snake_x, snake_y)
        world.add_entity(snake)

        # Positionner la pomme verte à la tête du serpent pour la "manger"
        green_apple.teleport(snake_x, snake_y)
        world.add_entity(green_apple)
        
        # Dans votre implémentation, 'eat' est appelée APRÈS que le serpent ait bougé sur l'apple.
        # Le benchmark de 'eat' seul signifie que la pomme doit être à la position de la tête.
        return (green_apple,), {} # La méthode eat prend l'apple en argument
    
    benchmark.pedantic(snake.eat, setup=setup_eat_green, rounds=100)

def test_snake_eat_red_apple_benchmark(benchmark, long_snake, red_apple):
    """Benchmark de la consommation d'une pomme rouge (implique perte de segment)."""
    def setup_eat_red():
        world = long_snake._Snake__world
        world._World__entities = []
        
        snake_x, snake_y = world.get_width() // 2, world.get_height() // 2
        long_snake.teleport(snake_x, snake_y)
        world.add_entity(long_snake)
        
        # S'assurer que le serpent a au moins 1 segment de corps pour pouvoir en perdre un.
        # Le Snake init déjà le serpent avec 2 segments de corps.
        
        # Positionner la pomme rouge à la tête
        red_apple.teleport(snake_x, snake_y)
        world.add_entity(red_apple)
        
        return (red_apple,), {}
    
    benchmark.pedantic(long_snake.eat, setup=setup_eat_red, rounds=100)


def test_snake_get_state_at_benchmark(benchmark, snake):
    """Benchmark de la méthode get_state_at du serpent."""
    def setup_get_state_at():
        # Tester à une position aléatoire valide
        world = snake._Snake__world
        x = random.randint(1, world.get_width() - 1)
        y = random.randint(1, world.get_height() - 1)
        return (x, y), {}
    
    benchmark.pedantic(snake.get_state_at, setup=setup_get_state_at, rounds=1000)

def test_snake_see_benchmark(benchmark, snake):
    """Benchmark de la méthode see() du serpent (vision du serpent)."""
    # Votre méthode see parcourt les lignes et colonnes passant par la tête
    def setup_see():
        world = snake._Snake__world
        world._World__entities = [snake] # Réinitialiser le monde avec juste le serpent
        
        # Ajouter quelques pommes aléatoires pour un scénario plus réaliste pour 'see'
        empty_locs = world.get_empty_locations()
        num_apples_to_add = min(5, len(empty_locs)) # Ajouter max 5 pommes
        
        for _ in range(num_apples_to_add):
            if empty_locs:
                apple_pos = random.choice(empty_locs)
                temp_apple = Apple(world, random.choice([AppleType.RED, AppleType.GREEN]))
                temp_apple.teleport(apple_pos[0], apple_pos[1])
                world.add_entity(temp_apple)
                empty_locs.remove(apple_pos) # Éviter de placer 2x au même endroit
        return (), {}
    
    benchmark.pedantic(snake.see, setup=setup_see, rounds=100)

def test_snake_get_state_benchmark(benchmark, snake):
    """Benchmark de la méthode get_state() du serpent (état booléen)."""
    def setup_get_state():
        world = snake._Snake__world
        world._World__entities = [snake]
        
        # Ajouter des entités pour que l'état soit non-trivial
        empty_locs = world.get_empty_locations()
        num_items_to_add = min(5, len(empty_locs))
        for _ in range(num_items_to_add):
            if empty_locs:
                item_pos = random.choice(empty_locs)
                # Ajout de pommes pour tester la logique de get_state
                item = Apple(world, random.choice([AppleType.RED, AppleType.GREEN]))
                item.teleport(item_pos[0], item_pos[1])
                world.add_entity(item)
                empty_locs.remove(item_pos)
        return (), {}
    
    benchmark.pedantic(snake.get_state, setup=setup_get_state, rounds=100)

def test_snake_contains_point_benchmark(benchmark, long_snake):
    """Benchmark de la méthode contains_point() du serpent (pour la tête et le corps)."""
    # Utiliser un long_snake pour bien tester la recherche dans le corps
    def setup_contains_point():
        # Points à tester: tête, un segment du corps, et un point hors du serpent
        head_x, head_y = long_snake.get_position()
        if long_snake.get_body():
            body_x, body_y = random.choice(long_snake.get_body())
        else:
            body_x, body_y = head_x, head_y # Fallback si le corps est vide

        points_to_test = [
            (head_x, head_y),
            (body_x, body_y),
            (0, 0) # Un point sûr hors du serpent
        ]
        # Choisissez un point aléatoire pour ce round
        test_x, test_y = random.choice(points_to_test)
        return (test_x, test_y), {}
    
    benchmark.pedantic(long_snake.contains_point, setup=setup_contains_point, rounds=1000)

def test_snake_render_benchmark(benchmark, long_snake):
    """Benchmark de la méthode render du serpent."""
    benchmark(long_snake.render)