import pygame
from ..display import draw_text, JAUNE


def pause_menu(screen: pygame.Surface) -> None:
    """Draws the PAUSE text. The caller owns the pause loop."""
    centre = (screen.get_width() // 2, screen.get_height() // 2)
    draw_text(screen, "PAUSE", 60, centre, JAUNE)
    draw_text(screen, "Press n to skip the level", 30,
              (centre[0], centre[1] + 60), JAUNE)
    draw_text(screen, "Press n to skip the level", 30,
              (centre[0], centre[1] + 60), JAUNE)
