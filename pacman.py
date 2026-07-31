from src.engine import Engine
from src.renderer import press_start, draw_maze
from mazegenerator import MazeGenerator
import random
import pygame

MAZE_SIZE = (20, 10)


def new_maze() -> list[list[int]]:
    """Generates a fresh maze with a random seed."""
    return MazeGenerator(size=MAZE_SIZE, seed=random.randint(0, 1000)).maze


maze = new_maze()
height = len(maze) * 40 + 60
width = len(maze[0]) * 40
pygame.init()
screen = pygame.display.set_mode((width, height))
press_start(screen)

replay = True
while replay:
    replay = Engine(maze, screen, draw_maze(maze)).run()
    if replay:
        maze = new_maze()
pygame.quit()
