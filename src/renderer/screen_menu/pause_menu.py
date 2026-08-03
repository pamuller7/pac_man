import pygame
from ..display import draw_text, JAUNE


RED = (255, 0, 0)


def pause_menu(screen: pygame.Surface, player: "PacMan") -> None:
    """Draws the PAUSE text. The caller owns the pause loop."""
    centre = (screen.get_width() // 2, screen.get_height() // 2)
    draw_text(screen, "PAUSE", 60, centre, RED)
    draw_text(screen, "-> n to skip the level", 30,
              (centre[0], centre[1] + 60), RED)
    if player.god_mod:
        god_txt = "-> g to disable god mod"
    else:
        god_txt = "-> g to enable god mod"
    draw_text(screen, god_txt, 30,
              (centre[0], centre[1] + 80), RED)
    draw_text(screen, "-> escape to go to the menu", 30,
              (centre[0], centre[1] + 100), RED)
