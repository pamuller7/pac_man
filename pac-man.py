"""Entry point.

Usage:
    python3 pac-man.py config.json

Every failure is reported as a one-line message on stderr, never as a
Python traceback, and exits with EXIT_FAILURE.
"""

import random
import sys
from time import time
from typing import List, Tuple
import pygame
from src.entities import PacMan
from src.error import NoSpawnError
from mazegenerator import MazeGenerator
from src.config import Config, Level, load_config
from src.engine import Engine
from src.error import PacManError
from src.player import Scoreboard
from src.renderer import (HUD_HEIGHT, CELL_SIZE, ask_name, display_endgame,
                          draw_maze, main_menu)

TOP_SHOWN = 5
USAGE = "usage: python3 pac-man.py config.json"


def find_spawn(maze: List[List[int]]) -> Tuple[int, int]:
    """Returns (col, row) of the walkable cell nearest the maze center.

    Cells with value 15 have walls on all four sides (solid blocks), so
    Pac-Man must not spawn there or he would be unable to move.

    Raises:
        NoSpawnError: if every cell is a solid wall block.
    """
    rows, cols = len(maze), len(maze[0])
    center_x, center_y = cols // 2, rows // 2
    best, best_dist = None, None
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] != 15:
                dist = (x - center_x) ** 2 + (y - center_y) ** 2
                if best_dist is None or dist < best_dist:
                    best, best_dist = (x, y), dist
    if best is None:
        raise NoSpawnError()
    return best


def new_maze(level: Level) -> List[List[int]]:
    """Generates a fresh maze of the size asked by `level`."""
    maze: List[List[int]] = MazeGenerator(
        size=(level.width, level.height),
        seed=level.seed).maze
    return maze


def open_window(level: Level, max_height: int, max_width: int,
                screen: pygame.Surface | None = None) -> pygame.Surface:
    """Opens (or resizes) the window so `level` fits in it.

    A `screen` already at the right size is kept as is: two levels of the
    same size must go on without the window blinking between them.
    """
    width = max_width * CELL_SIZE
    height = max_height * CELL_SIZE + HUD_HEIGHT
    if screen is not None and screen.get_size() == (width, height):
        return screen
    return pygame.display.set_mode((width, height))


def play_run(screen: pygame.Surface,
             config: Config, max_height: int,
             max_width: int,
             sprite_cache: dict[tuple[str, int], pygame.Surface]
             ) -> Tuple[bool, int, pygame.Surface]:
    """Plays the levels in order until one is lost or all are cleared.

    Returns (won, total score, window), the window being returned because
    it is rebuilt whenever a level has a different size.
    """
    total = 0
    pacman = PacMan(0, 0,
                    maze_infos=(0, 0),
                    hp=config.lives)
    level_number = 0
    max_width = max(var.width for var in config.levels)
    max_height = max(var.height for var in config.levels)
    while level_number < config.max_nb_level:
        level = config.levels[level_number]
        level_number += 1
        maze = new_maze(level)
        spawn_col, spawn_row = find_spawn(maze)
        maze_infos = (len(maze[0]) - 1, len(maze) - 1)
        pacman.set_init_pos(spawn_col, spawn_row, maze_infos)
        screen = open_window(level, max_height, max_width, screen)
        won, score = Engine(maze=maze,
                            player=pacman,
                            sprite_cache=sprite_cache,
                            screen=screen,
                            maze_surface=draw_maze(maze),
                            config=config,
                            level=level,
                            level_number=level_number).run()
        pacman.targetable = True
        pacman.eats_everything = False
        pacman.chase_swich = time()
        total = pacman.score
        if not won:
            return False, total, screen
        if level_number == len(config.levels):
            new_level = Level(
                width=random.randint(15, max_width),
                height=random.randint(15, max_height),
                seed=random.randint(0, 100000),
            )
            config.levels.append(new_level)
    return True, total, screen


def game_loop(config: Config) -> None:
    """Menu -> game -> name entry, until the player leaves."""
    board = Scoreboard(config.highscore_filename)
    board.load()
    max_width = max(var.width for var in config.levels)
    max_height = max(var.height for var in config.levels)
    sprite_cache: dict[tuple[str, int], pygame.Surface] = dict()
    screen = open_window(config.levels[0], max_height, max_width)
    while main_menu(screen, board.top(TOP_SHOWN)):
        won, score, screen = play_run(screen, config, max_height,
                                      max_width, sprite_cache)
        if not display_endgame(screen, score, won):
            break
        name = ask_name(screen, won, score)
        if name:
            board.add_score(board.get_player(name), score)
            board.save()


def main(argv: List[str]) -> int:
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
        print("Default values will be used - cf README.md, config section")
        config = Config()
    try:
        pygame.init()
        game_loop(config)
    except PacManError as exc:
        print(f"\033[31m[Error]\033[0m pac-man: {exc}", file=sys.stderr)
        return 1
    except pygame.error as exc:
        print(f"\033[31m[Error]\033[0m pac-man: display error: {exc}",
              file=sys.stderr)
        return 1
    finally:
        pygame.quit()
    return 0


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("goodbye!!!!")
