import pygame

CELL_SIZE = 40
N, E, S, W = 1, 2, 4, 8
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HUD_HEIGHT = 50

_FONT_CACHE: dict[int, pygame.font.Font] = {}


def get_font(taille: int) -> pygame.font.Font:
    """Returns a cached pygame Font for the given size."""
    if taille not in _FONT_CACHE:
        _FONT_CACHE[taille] = pygame.font.Font(None, taille)
    return _FONT_CACHE[taille]


def draw_text(surface: pygame.Surface, texte: str, taille: int,
              position: tuple[int, int],
              couleur: tuple[int, int, int] = YELLOW,
              centre: bool = True) -> pygame.Rect:
    """
    Rends du texte et le blit sur la surface.
    """
    font = get_font(taille)
    rendu = font.render(texte, True, couleur)
    if centre:
        rect = rendu.get_rect(center=position)
    else:
        rect = rendu.get_rect(topleft=position)
    surface.blit(rendu, rect)
    return rect


def draw_cell(surface: pygame.Surface, col: int, ligne: int,
              valeur: int) -> None:
    """Draws one maze cell (walls) onto the maze surface, pixel by pixel."""
    start_x = col * CELL_SIZE
    start_y = ligne * CELL_SIZE
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            couleur = None
            if i == 0 and (valeur & N):
                couleur = (0, 0, 255)
            elif i == CELL_SIZE - 1 and (valeur & S):
                couleur = (0, 0, 255)
            elif j == 0 and (valeur & W):
                couleur = (0, 0, 255)
            elif j == CELL_SIZE - 1 and (valeur & E):
                couleur = (0, 0, 255)
            if couleur:
                surface.set_at((start_x + j, start_y + i), couleur)


def draw_maze(maze: list[list[int]]) -> pygame.Surface:
    """Builds the full maze as one static Surface (drawn once)."""
    height = len(maze) * CELL_SIZE
    width = len(maze[0]) * CELL_SIZE
    surface = pygame.Surface((width, height))

    for i, row in enumerate(maze):
        for j, valeur in enumerate(row):
            draw_cell(surface, j, i, valeur)
    return surface
