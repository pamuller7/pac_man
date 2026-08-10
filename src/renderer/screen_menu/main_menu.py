import pygame
from src.player.player import Player
from src.renderer.display import draw_text, YELLOW, BLACK
from path import resource_path
import os
from src.error import AssetNotFoundError, AssetError


def load_sprite(relative_path: str, screen: pygame.Surface) -> pygame.Surface:
    """Loads and scales a sprite to one cell.

    Raises:
        AssetNotFoundError: if the file does not exist.
        AssetError: if pygame fails to decode it.
    """
    path = resource_path(relative_path)
    if not os.path.exists(path):
        raise AssetNotFoundError(path)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as exc:
        raise AssetError(path, str(exc)) from exc
    image = pygame.image.load(path).convert_alpha()
    dim = (screen.get_width(), screen.get_height())
    return pygame.transform.scale(image, dim)


def instructions_menu(screen: pygame.Surface) -> None:
    """Displays the game instructions until the user presses a key."""
    centre_x = screen.get_width() // 2
    screen.fill(BLACK)
    try:
        screen.blit(load_sprite("assets/menu.png", screen), (0, 80))
    except (AssetNotFoundError, AssetError):
        pass
    draw_text(screen, "INSTRUCTIONS", 50, (centre_x, 60), YELLOW)
    instructions = [
        "Arrow keys or [w,a,s,d] : Move Pac-Man",
        "Eat all pacgums to complete the level.",
        "Super pacgums allow you to eat ghosts.",
        "Avoid ghosts while they are not vulnerable.",
        "",
        "SPACE or ESC : Return to the main menu",
    ]

    y = 140
    for line in instructions:
        draw_text(screen, line, 28, (centre_x, y), YELLOW)
        y += 40
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_SPACE,
                ):
                    return


def main_menu(screen: pygame.Surface,
              scores: list[Player] | None = None) -> bool:
    """Displays the main menu. Returns False if the player quits.

    `scores` is the (name, score) ranking to show, best first; an empty
    or missing ranking simply hides the board.
    """
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2
    pygame.event.clear()
    scores = sorted(scores,
                    key=lambda player: player.best_score,
                    reverse=True) if scores else None
    while True:
        screen.fill(BLACK)
        try:
            screen.blit(load_sprite("assets/menu.png", screen), (0, 80))
        except (AssetNotFoundError, AssetError):
            pass
        draw_text(screen, "PAC-MAN", 60, (centre_x, centre_y - 120), YELLOW)
        draw_text(screen, "ESPACE : JOUER   -   ECHAP : QUITTER", 30,
                  (centre_x, centre_y - 60), YELLOW)
        draw_text(screen, "I : INSTRUCTIONS", 30,
                  (centre_x, centre_y - 10), YELLOW)
        if scores:
            draw_text(screen, "MEILLEURS SCORES", 30,
                      (centre_x, centre_y + 60), YELLOW)
            for rank, player in enumerate(scores):
                draw_text(screen, f"{rank + 1}. \
{player.name} - {player.best_score}", 25,
                          (centre_x, centre_y + 100 + rank * 25), YELLOW)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_i:
                    instructions_menu(screen)
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return True
