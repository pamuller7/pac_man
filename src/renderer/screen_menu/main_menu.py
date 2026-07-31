import pygame
from ..display import draw_text, JAUNE, NOIR


def main_menu(screen: pygame.Surface) -> None:
    """Displays the main menu and waits for any key press."""
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2

    screen.fill(NOIR)
    draw_text(screen, "PAC-MAN", 60, (centre_x, centre_y - 40), JAUNE)
    draw_text(screen, "APPUYEZ SUR UNE TOUCHE POUR JOUER", 30,
              (centre_x, centre_y + 20), JAUNE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                waiting = False
