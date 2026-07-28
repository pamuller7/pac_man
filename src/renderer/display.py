import pygame

TAILLE_CASE = 40
N, E, S, W = 1, 2, 4, 8


def loading_screen(screen: pygame.Surface, message: str = "Loading...",
                    duration_ms: int = 2000) -> None:
    """Displays a simple loading screen for a fixed duration."""
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2,
                                        screen.get_height() // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    pygame.time.delay(duration_ms)

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

    loading_screen(surface, "Loading maze...", 2000)
    for i, row in enumerate(maze):
        for j, valeur in enumerate(row):
            draw_cell(surface, j, i, valeur)
    return surface



def draw_menu():
    pass
