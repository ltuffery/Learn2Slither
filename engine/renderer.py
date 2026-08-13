import pygame
import engine.settings as settings
from engine.entity.snake import Snake
from engine.entity.apple import Apple


class PygameRenderer:
    """
    A singleton renderer that draws the game world using pygame.

    Replaces the terminal-based rendering with a graphical window.
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._initialized = False
        self.screen = None
        self.font = None
        self._cell = settings.CELL_SIZE
        self._cols = 0
        self._rows = 0
        self._title_h = 40
        self._grid_w = 0
        self._gap = 20

    def _init(self):
        if self._initialized:
            return

        pygame.init()
        pygame.display.set_caption("Learn2Slither")

        self._cell = settings.CELL_SIZE
        self._cols = settings.WIDTH + 2
        self._rows = settings.HEIGHT + 2

        self._grid_w = self._cols * self._cell
        grid_h = self._rows * self._cell
        self._gap = 20

        total_w = self._grid_w
        total_h = self._title_h + grid_h

        self.screen = pygame.display.set_mode((total_w, total_h))
        self.font = pygame.font.Font(None, 24)
        self._initialized = True

    def _draw_cell(self, x, y, color, offset_x=0, offset_y=0):
        margin = 1
        pygame.draw.rect(
            self.screen,
            color,
            (
                offset_x + x * self._cell + margin,
                offset_y + y * self._cell + margin,
                self._cell - 2 * margin,
                self._cell - 2 * margin,
            ),
        )

    def render(self, world, title=None):
        self._init()

        self.screen.fill(settings.COLOR_BG)

        snake = None
        for entity in world.get_entities():
            if isinstance(entity, Snake):
                snake = entity
                break

        grid_offset_y = self._title_h

        if title:
            text_surf = self.font.render(title, True, settings.COLOR_TEXT)
            self.screen.blit(text_surf, (10, 4))

        if snake:
            dir_surf = self.font.render(
                f"Direction: {snake.get_last_direction().name}",
                True,
                settings.COLOR_TEXT,
            )
            self.screen.blit(dir_surf, (10, 22))

        for x in range(self._cols):
            self._draw_cell(x, 0, settings.COLOR_WALL, 0, grid_offset_y)
            self._draw_cell(
                x, self._rows - 1, settings.COLOR_WALL, 0, grid_offset_y
            )
        for y in range(1, self._rows - 1):
            self._draw_cell(0, y, settings.COLOR_WALL, 0, grid_offset_y)
            self._draw_cell(
                self._cols - 1, y, settings.COLOR_WALL, 0, grid_offset_y
            )

        for entity in world.get_entities():
            if isinstance(entity, Snake):
                hx, hy = entity.get_position()
                self._draw_cell(
                    hx, hy, settings.COLOR_SNAKE_HEAD, 0, grid_offset_y
                )
                for bx, by in entity.get_body():
                    self._draw_cell(
                        bx, by, settings.COLOR_SNAKE_BODY, 0, grid_offset_y
                    )
            elif isinstance(entity, Apple):
                ax, ay = entity.get_position()
                color = (
                    settings.COLOR_GREEN_APPLE
                    if entity.is_green()
                    else settings.COLOR_RED_APPLE
                )
                self._draw_cell(ax, ay, color, 0, grid_offset_y)

        pygame.display.flip()

    @classmethod
    def quit(cls):
        if cls._instance is not None and cls._instance._initialized:
            pygame.quit()
            cls._instance = None
