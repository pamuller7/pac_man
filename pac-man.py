"""Entry point.

Usage:
    python3 pac-man.py config.json

Every failure is reported as a one-line message on stderr, never as a
Python traceback, and exits with EXIT_FAILURE.
"""

import random
import sys

import pygame
from mazegenerator import MazeGenerator

from src.config import Config, Level, load_config
from src.engine import Engine
from src.error import PacManError
from src.player import Scoreboard
from src.renderer import (HUD_HEIGHT, TAILLE_CASE, ask_name, display_endgame,
                          draw_maze, main_menu)

TOP_SHOWN = 5
USAGE = "usage: python3 pac-man.py config.json"


def new_maze(level: Level) -> list[list[int]]:
    """Generates a fresh maze of the size asked by `level`."""
    maze: list[list[int]] = MazeGenerator(
        size=(level.width, level.height),
        seed=random.randint(0, 1000)).maze
    return maze


def open_window(level: Level,
                screen: pygame.Surface | None = None) -> pygame.Surface:
    """Opens (or resizes) the window so `level` fits in it.

    A `screen` already at the right size is kept as is: two levels of the
    same size must go on without the window blinking between them.
    """
    width = level.width * TAILLE_CASE
    height = level.height * TAILLE_CASE + HUD_HEIGHT
    if screen is not None and screen.get_size() == (width, height):
        return screen
    return pygame.display.set_mode((width, height))


def play_run(screen: pygame.Surface,
             config: Config) -> tuple[bool, int, pygame.Surface]:
    """Plays the levels in order until one is lost or all are cleared.

    Returns (won, total score, window), the window being returned because
    it is rebuilt whenever a level has a different size.
    """
    total = 0
    for level in config.levels:
        maze = new_maze(level)
        screen = open_window(level, screen)
        won, score = Engine(maze, screen, draw_maze(maze),
                            config, level).run()
        total += score
        if not won:
            return False, total, screen
    return True, total, screen


def game_loop(config: Config) -> None:
    """Menu -> game -> name entry, until the player leaves."""
    board = Scoreboard(config.highscore_filename)
    board.load()
    screen = open_window(config.levels[0])
    while main_menu(screen, board.top(TOP_SHOWN)):
        won, score, screen = play_run(screen, config)
        if not display_endgame(screen, score, won):
            break
        name = ask_name(screen, score)
        if name:
            board.add_score(board.get_player(name), score)
            board.save()


def main(argv: list[str]) -> int:
    """Checks the arguments, loads the config and runs the game."""
    if len(argv) != 2:
        print(f"{USAGE}: expected 1 argument, got {len(argv) - 1}.",
              file=sys.stderr)
        return 1
    if argv[1] in ("-h", "--help"):
        print(USAGE)
        return 1
    try:
        config = load_config(argv[1])
    except PacManError as exc:
        print(f"pac-man: {exc}", file=sys.stderr)
        return 1
    try:
        pygame.init()
        game_loop(config)
    except PacManError as exc:
        print(f"pac-man: {exc}", file=sys.stderr)
        return 1
    except pygame.error as exc:
        print(f"pac-man: display error: {exc}", file=sys.stderr)
        return 1
    finally:
        pygame.quit()
    return 0


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("goodbye!!!!")
