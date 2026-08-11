import pygame
from ..display import draw_text, YELLOW, BLACK


def press_start(screen: pygame.Surface) -> None:
    """Displays a title screen and waits for any key press."""
    center = (screen.get_width() // 2, screen.get_height() // 2)

    screen.fill(BLACK)
    draw_text(screen, "PRESS START", 60, center, YELLOW)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                waiting = False
