from src.engine import Engine
from src.renderer import main_menu, display_endgame, ask_name, draw_maze
from src.player import Scoreboard
from mazegenerator import MazeGenerator
import random
import pygame

MAZE_SIZE = (20, 10)
TOP_SHOWN = 5


def new_maze() -> list[list[int]]:
    """Generates a fresh maze with a random seed."""
    return MazeGenerator(size=MAZE_SIZE, seed=random.randint(0, 1000)).maze


maze = new_maze()
height = len(maze) * 40 + 60
width = len(maze[0]) * 40
pygame.init()
screen = pygame.display.set_mode((width, height))

board = Scoreboard()
board.load()

while main_menu(screen, board.top(TOP_SHOWN)):
    maze = new_maze()
    won, score = Engine(maze, screen, draw_maze(maze)).run()
    if not display_endgame(screen, score, won):
        break
    name = ask_name(screen, score)
    if name:
        board.add_score(board.get_player(name), score)
        board.save()
pygame.quit()
