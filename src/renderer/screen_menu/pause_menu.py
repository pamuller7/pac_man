import pygame
from ..display import draw_text, JAUNE
from typing import Any

RED = (255, 0, 0)

import pygame
from ..display import draw_text, JAUNE


RED = (255, 0, 0)


def pause_menu(screen: pygame.Surface, player: Any, ghosts: Any) -> None:
    """Draws the PAUSE text. The caller owns the pause loop."""
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    centre = (screen.get_width() // 2, screen.get_height() // 2)
    line_height = 35

    draw_text(screen, "PAUSE", 60, centre, RED)
    draw_text(screen, "-> n to skip the level", 30,
              (centre[0], centre[1] + line_height * 1), RED)
    if player.god_mod:
        god_info = "disable"
    else:
        god_info = "enable"
    god_txt = f"-> g to {god_info} god mod"
    if ghosts[0].freeze:
        freeze_info = "unfreeze"
    else:
        freeze_info = "freeze"
    draw_text(screen, god_txt, 30,
              (centre[0], centre[1] + line_height * 2), RED)
    draw_text(screen, "-> escape to go to the menu", 30,
              (centre[0], centre[1] + line_height * 3), RED)
    draw_text(screen, f"-> f to {freeze_info} ghosts", 30,
              (centre[0], centre[1] + line_height * 4), RED)
    draw_text(screen, f"-> h to increase hp. current: {player.hp}", 30,
              (centre[0], centre[1] + line_height * 5), RED)
