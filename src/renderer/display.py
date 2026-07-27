from abc import abstractmethod, ABC
import pygame

TAILLE_CASE = 40
N, E, S, W = 1, 2, 4, 8



class DrawCharacter(ABC):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    @abstractmethod
    def create(self):
        if self.name == "Pac-Man":
            # Create Pac-Man character
            pass
        if self.name == "ghost":
            # Create ghost character
            pass


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
            surface.set_at((start_x + j, start_y + i),
                                                 couleur)


def draw_maze(maze: list[list[int]]) -> pygame.Surface:
    """Builds the full maze as one static Surface (drawn once)."""
    height = len(maze) * TAILLE_CASE
    width = len(maze[0]) * TAILLE_CASE
    surface = pygame.Surface((width, height))

    for i, row in enumerate(maze):
        for j, valeur in enumerate(row):
            draw_cell(surface, j, i, valeur)
    return surface


def display_maze(maze: list[list[int]]) -> None:
    """Displays maze and Pac-Man using pygame."""
    pygame.init()
    pygame.display.set_caption("ᗧ Pac-Man ᗧ")

    height = len(maze) * TAILLE_CASE
    width = len(maze[0]) * TAILLE_CASE
    screen = pygame.display.set_mode((width, height))

    maze_surface = draw_maze(maze)

    pac_img = pygame.image.load("assets/pacman.png").convert_alpha()
    pac_img = pygame.transform.scale(pac_img, (TAILLE_CASE, TAILLE_CASE))

    pac_x, pac_y = 20, 20

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(maze_surface, (0, 0))
        screen.blit(pac_img, (pac_x - TAILLE_CASE // 2,
                               pac_y - TAILLE_CASE // 2))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()