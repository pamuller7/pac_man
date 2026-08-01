import pygame
from ..display import draw_text, JAUNE, NOIR


def main_menu(screen: pygame.Surface,
              scores: list[tuple[str, int]] | None = None) -> bool:
    """Displays the main menu. Returns False if the player quits.

    `scores` is the (name, score) ranking to show, best first; an empty
    or missing ranking simply hides the board.
    """
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2

    screen.fill(NOIR)
    draw_text(screen, "PAC-MAN", 60, (centre_x, centre_y - 120), JAUNE)
    draw_text(screen, "ESPACE : JOUER   -   ECHAP : QUITTER", 30,
              (centre_x, centre_y - 60), JAUNE)

    if scores:
        draw_text(screen, "MEILLEURS SCORES", 30, (centre_x, centre_y), JAUNE)
        for rank, (name, score) in enumerate(scores):
            draw_text(screen, f"{rank + 1}. {name} - {score}", 25,
                      (centre_x, centre_y + 35 + rank * 25), JAUNE)
    pygame.display.flip()

    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return True
