from src.renderer import display_maze
from mazegenerator import MazeGenerator

mg = MazeGenerator(size=(100, 100), seed=42)

for row in mg.maze:
    for cell in row:
        print(cell, end=" ")
    print()

display_maze(mg.maze)