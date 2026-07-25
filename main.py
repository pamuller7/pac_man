import pyglet
from pyglet import shapes

CELL_SIZE = 1000
N, E, S, W = 1, 2, 4, 8

def build_maze_shapes(maze, batch):
    """Convertit la grille en une liste de segments (murs) à dessiner."""
    lines = []
    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            # coordonnées du coin haut-gauche de la cellule
            px = x * CELL_SIZE
            # pyglet a l'origine en bas-gauche -> on inverse y
            py = (height - 1 - y) * CELL_SIZE

            if cell & N:
                lines.append(shapes.Line(px, py + CELL_SIZE,
                                          px + CELL_SIZE, py + CELL_SIZE,
                                          thickness=2, color=(0, 100, 255),
                                          batch=batch))
            if cell & S:
                lines.append(shapes.Line(px, py,
                                          px + CELL_SIZE, py,
                                          thickness=2, color=(0, 100, 255),
                                          batch=batch))
            if cell & W:
                lines.append(shapes.Line(px, py,
                                          px, py + CELL_SIZE,
                                          thickness=2, color=(0, 100, 255),
                                          batch=batch))
            if cell & E:
                lines.append(shapes.Line(px + CELL_SIZE, py,
                                          px + CELL_SIZE, py + CELL_SIZE,
                                          thickness=2, color=(0, 100, 255),
                                          batch=batch))
    return lines


# ---- Exemple d'utilisation ----
from mazegenerator import MazeGenerator

mg = MazeGenerator(size=(15, 15), seed=1)
maze = mg.maze

window = pyglet.window.Window(
    width=len(maze[0]) * CELL_SIZE,
    height=len(maze) * CELL_SIZE,
    caption="Pac-Man Maze"
)

batch = pyglet.graphics.Batch()
# IMPORTANT: garder une référence aux lignes, sinon elles sont
# garbage-collectées et disparaissent de l'écran !
wall_lines = build_maze_shapes(maze, batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()