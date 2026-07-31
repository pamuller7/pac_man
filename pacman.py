from src.engine import Engine
from src.renderer import press_start
from mazegenerator import MazeGenerator
import pygame

mg = MazeGenerator(size=(10, 10), seed=42)

for row in mg.maze:
    for cell in row:
        print(cell, end=" ")
    print()

height = len(mg.maze) * 40
width = len(mg.maze[0]) * 40
pygame.init()
screen = pygame.display.set_mode((width, height)) 
press_start(screen)

replay = True
while replay:
    replay = Engine(mg.maze).run()
pygame.quit()