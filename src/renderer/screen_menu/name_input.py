import pygame
from ..display import draw_text, NOIR, JAUNE
from ...player import NAME_MAX_LENGTH
from .main_menu import load_sprite
from ...error import AssetNotFoundError, AssetError


ASSETS = ["assets/win.png", "assets/loose.png"]


def ask_name(screen: pygame.Surface, won: int, score: int = 0) -> str | None:
    """Asks the player for a name to store the score under.

    Returns the typed name, or None if the player cancels or closes the
    window. The name is capped at NAME_MAX_LENGTH so the scoreboard never
    has to reject it.
    """
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2
    name = ""

    pygame.event.clear()
    pygame.key.start_text_input()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.TEXTINPUT:
                    if len(name) + len(event.text) <= NAME_MAX_LENGTH:
                        name += event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip()

            screen.fill(NOIR)
            sprite = ASSETS[0] if won else ASSETS[1]
            try:
                screen.blit(load_sprite(sprite, screen), (0, 10))
            except (AssetNotFoundError, AssetError):
                pass
            draw_text(screen, f"SCORE : {score}", 30,
                      (centre_x, centre_y - 80), JAUNE)
            draw_text(screen, "ENTREZ VOTRE NOM", 40,
                      (centre_x, centre_y - 30), JAUNE)
            draw_text(screen, f"{name}_", 40, (centre_x, centre_y + 20),
                      JAUNE)
            draw_text(screen, "ENTREE : VALIDER   -   ECHAP : PASSER", 25,
                      (centre_x, centre_y + 80), JAUNE)
            pygame.display.flip()
    finally:
        pygame.key.stop_text_input()
