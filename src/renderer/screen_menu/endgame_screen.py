import pygame
from ..display import draw_text, NOIR, JAUNE


def display_endgame(screen: pygame.Surface, score: int = 0) -> bool:
    """Displays the endgame screen. Returns True if the player restarts."""
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2

    screen.fill(NOIR)

    draw_text(screen, "GAME OVER", 60, (centre_x, centre_y - 45), JAUNE)
    draw_text(screen, f"SCORE : {score}", 30, (centre_x, centre_y), JAUNE)
    draw_text(screen, "ESPACE : REJOUER   -   ECHAP : QUITTER", 30,
              (centre_x, centre_y + 50), JAUNE)
    pygame.display.flip()

    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
