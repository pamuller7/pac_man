import pygame
from ..display import draw_text, BLACK, YELLOW
from .main_menu import load_sprite
from ...error import AssetNotFoundError, AssetError

ASSETS = ["assets/win.png", "assets/loose.png"]


def display_endgame(screen: pygame.Surface, score: int = 0,
                    won: bool = False) -> bool:
    """Displays the endgame screen. Returns False if the player quits.

    True means "carry on with the flow" (score entry, then main menu).
    """
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2

    screen.fill(BLACK)

    titre = "YOU WIN" if won else "GAME OVER"
    sprite = ASSETS[0] if won else ASSETS[1]
    try:
        screen.blit(load_sprite(sprite, screen), (0, 10))
    except (AssetNotFoundError, AssetError):
        pass
    draw_text(screen, titre, 60, (centre_x, centre_y - 45), YELLOW)
    draw_text(screen, f"SCORE : {score}", 30, (centre_x, centre_y), YELLOW)
    draw_text(screen, "ESPACE : CONTINUER   -   ECHAP : QUITTER", 30,
              (centre_x, centre_y + 50), YELLOW)
    pygame.display.flip()

    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
