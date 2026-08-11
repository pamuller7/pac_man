import pygame

CELL_SIZE = 40
N, E, S, W = 1, 2, 4, 8
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HUD_HEIGHT = 50

_FONT_CACHE: dict[int, pygame.font.Font] = {}


def get_font(size: int) -> pygame.font.Font:
    """Returns a cached pygame Font for the given size."""
    if size not in _FONT_CACHE:
        _FONT_CACHE[size] = pygame.font.Font(None, size)
    return _FONT_CACHE[size]


def draw_text(surface: pygame.Surface, texte: str, size: int,
              position: tuple[int, int],
              color: tuple[int, int, int] = YELLOW,
              center: bool = True) -> pygame.Rect:
    """
    Rends du texte et le blit sur la surface.
    """
    font = get_font(size)
    rendu = font.render(texte, True, color)
    if center:
        rect = rendu.get_rect(center=position)
    else:
        rect = rendu.get_rect(topleft=position)
    surface.blit(rendu, rect)
    return rect


def draw_cell(surface: pygame.Surface, col: int, line: int,
              valeur: int) -> None:
    """Draws one maze cell (walls) onto the maze surface, pixel by pixel."""
    start_x = col * CELL_SIZE
    start_y = line * CELL_SIZE
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            color = None
            if i == 0 and (valeur & N):
                color = (0, 0, 255)
            elif i == CELL_SIZE - 1 and (valeur & S):
                color = (0, 0, 255)
            elif j == 0 and (valeur & W):
                color = (0, 0, 255)
            elif j == CELL_SIZE - 1 and (valeur & E):
                color = (0, 0, 255)
            if color:
                surface.set_at((start_x + j, start_y + i), color)


def draw_maze(maze: list[list[int]]) -> pygame.Surface:
    """Builds the full maze as one static Surface (drawn once)."""
    height = len(maze) * CELL_SIZE
    width = len(maze[0]) * CELL_SIZE
    surface = pygame.Surface((width, height))

    for i, row in enumerate(maze):
        for j, valeur in enumerate(row):
            draw_cell(surface, j, i, valeur)
    return surface
