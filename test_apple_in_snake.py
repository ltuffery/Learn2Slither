from engine.entity.apple import Apple, AppleType
from engine.game import Game

game = Game()
game.set_snake((1, 1), [(1, 2), (1, 3), (1, 4)])

world = game.get_world()
apple = Apple(world, AppleType.GREEN)

world.add_entity(apple)
game.get_snake().eat(apple)

print(game.get_snake().get_body())
print(game.get_snake().get_body()[-1] in world.get_empty_locations())

