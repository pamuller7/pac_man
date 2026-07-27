from src.engine import Engine
from mazegenerator import MazeGenerator

mg = MazeGenerator(size=(20, 20), seed=42)

for row in mg.maze:
    for cell in row:
        print(cell, end=" ")
    print()

Engine(mg.maze).run()