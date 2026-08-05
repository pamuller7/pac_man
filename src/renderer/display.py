import pygame

TAILLE_CASE = 40
N, E, S, W = 1, 2, 4, 8
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
EPAISSEUR = 3
HUD_HEIGHT = 50

_FONT_CACHE: dict[int, pygame.font.Font] = {}


def get_font(taille: int) -> pygame.font.Font:
    """Returns a cached pygame Font for the given size."""
    if taille not in _FONT_CACHE:
        _FONT_CACHE[taille] = pygame.font.Font(None, taille)
    return _FONT_CACHE[taille]


def draw_text(surface: pygame.Surface, texte: str, taille: int,
              position: tuple[int, int], couleur: tuple[int, int, int] = JAUNE,
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

# def draw_rect_pixel(surface: pygame.Surface,
#                     start_x: int, start_y: int,
#                     largeur: int, hauteur: int,
#                     couleur_bord: tuple = JAUNE,
#                     couleur_fond: tuple = NOIR,
#                     epaisseur: int = EPAISSEUR) -> None:
#     """Draws one rectangle onto the surface, pixel by pixel."""
#     surface.lock()
#     for i in range(hauteur):
#         for j in range(largeur):
#             couleur = couleur_fond
#             if i < epaisseur:
#                 couleur = couleur_bord
#             elif i >= hauteur - epaisseur:
#                 couleur = couleur_bord
#             elif j < epaisseur:
#                 couleur = couleur_bord
#             elif j >= largeur - epaisseur:
#                 couleur = couleur_bord
#             surface.set_at((start_x + j, start_y + i), couleur)
#     surface.unlock()


def draw_cell(surface: pygame.Surface, col: int, ligne: int,
              valeur: int) -> None:
    """Draws one maze cell (walls) onto the maze surface, pixel by pixel."""
    start_x = col * TAILLE_CASE
    start_y = ligne * TAILLE_CASE

    for i in range(TAILLE_CASE):
        for j in range(TAILLE_CASE):
            couleur = (0, 0, 0)
            if i == 0 and (valeur & N):
                couleur = (0, 0, 255)
            elif i == TAILLE_CASE - 1 and (valeur & S):
                couleur = (0, 0, 255)
            elif j == 0 and (valeur & W):
                couleur = (0, 0, 255)
            elif j == TAILLE_CASE - 1 and (valeur & E):
                couleur = (0, 0, 255)
            surface.set_at((start_x + j, start_y + i), couleur)


def draw_maze(maze: list[list[int]]) -> pygame.Surface:
    """Builds the full maze as one static Surface (drawn once)."""
    height = len(maze) * TAILLE_CASE
    width = len(maze[0]) * TAILLE_CASE
    surface = pygame.Surface((width, height))

    for i, row in enumerate(maze):
        for j, valeur in enumerate(row):
            draw_cell(surface, j, i, valeur)
    return surface
