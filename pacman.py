from src.renderer import display_maze
from mazegenerator import MazeGenerator

mg = MazeGenerator(size=(15, 15), seed=1)

for row in mg.maze:
    for cell in row:
        print(cell, end=" ")
    print()

display_maze(mg.maze)