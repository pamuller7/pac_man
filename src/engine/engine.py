import os

import pygame

from ..entities import PacMan
from ..error import (
    AssetError,
    AssetNotFoundError,
    EmptyMazeError,
    InvalidCellError,
    MalformedMazeError,
    NoSpawnError,
)
from ..renderer import TAILLE_CASE, draw_maze

PAC_SPRITE = "assets/pacman.png"

MOVE_INTERVAL = 150

KEY_TO_DIR = {
    pygame.K_UP: "N", pygame.K_w: "N",
    pygame.K_DOWN: "S", pygame.K_s: "S",
    pygame.K_LEFT: "W", pygame.K_a: "W",
    pygame.K_RIGHT: "E", pygame.K_d: "E",
}


def _slide(value: float, target: float, step: float) -> float:
    """Moves `value` toward `target` by at most `step` pixels."""
    if value < target:
        return min(value + step, target)
    if value > target:
        return max(value - step, target)
    return value


def validate_maze(maze: list[list[int]]) -> None:
    """Checks the maze grid before the game starts.

    Raises:
        EmptyMazeError: if the maze has no rows or no columns.
        MalformedMazeError: if the rows are not all the same length.
        InvalidCellError: if a cell is outside the 0..15 wall bitmask range.
    """
    if not maze or not maze[0]:
        raise EmptyMazeError()
    width = len(maze[0])
    for y, row in enumerate(maze):
        if len(row) != width:
            raise MalformedMazeError(expected=width, found=len(row), row=y)
        for x, value in enumerate(row):
            if not 0 <= value <= 15:
                raise InvalidCellError(value, (x, y))


def find_spawn(maze: list[list[int]]) -> tuple[int, int]:
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


class Engine:
    """Runs the game: window, Pac-Man sprite, input and the main loop.

    The maze background is drawn by the renderer; the engine owns everything
    that moves and the pygame lifecycle.
    """

    def __init__(self, maze: list[list[int]]) -> None:
        """Sets up the pygame window, maze surface and Pac-Man.

        Raises:
            MazeError: if the maze is empty, not rectangular or has bad cells.
            NoSpawnError: if the maze has no walkable spawn cell.
            AssetError: if the Pac-Man sprite cannot be loaded.
        """
        validate_maze(maze)
        self.maze = maze
        pygame.init()
        pygame.display.set_caption("ᗧ Pac-Man ᗧ")

        height = len(maze) * TAILLE_CASE
        width = len(maze[0]) * TAILLE_CASE
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.maze_surface = draw_maze(maze)
        self.pac_img = self._load_sprite(PAC_SPRITE)

        spawn_col, spawn_row = find_spawn(maze)
        self.pacman = PacMan(spawn_col, spawn_row)

        self.speed = TAILLE_CASE / (MOVE_INTERVAL / 1000)
        self.render_x = float(spawn_col * TAILLE_CASE)
        self.render_y = float(spawn_row * TAILLE_CASE)
        self.current_dir: str | None = None
        self.buffered_dir: str | None = None

    @staticmethod
    def _load_sprite(path: str) -> pygame.Surface:
        """Loads and scales a sprite to one cell.

        Raises:
            AssetNotFoundError: if the file does not exist.
            AssetError: if pygame fails to decode it.
        """
        if not os.path.exists(path):
            raise AssetNotFoundError(path)
        try:
            image = pygame.image.load(path).convert_alpha()
        except pygame.error as exc:
            raise AssetError(path, str(exc)) from exc
        return pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))

    def run(self) -> None:
        """Main loop: read time, read keys, move Pac-Man, draw."""
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            running = self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> bool:
        """Handles input; returns False when the window is closed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.buffered_dir = KEY_TO_DIR.get(
                    event.key, self.buffered_dir)
        return True

    def _update(self, dt: float) -> None:
        """Advances Pac-Man: step on the grid, then slide toward the cell."""
        target_x = self.pacman.pos.x * TAILLE_CASE
        target_y = self.pacman.pos.y * TAILLE_CASE

        if self.render_x == target_x and self.render_y == target_y:
            self._step()
            target_x = self.pacman.pos.x * TAILLE_CASE
            target_y = self.pacman.pos.y * TAILLE_CASE

        step = self.speed * dt
        self.render_x = _slide(self.render_x, target_x, step)
        self.render_y = _slide(self.render_y, target_y, step)

    def _step(self) -> None:
        """Chooses and applies the next grid move (buffered turn first)."""
        if self.buffered_dir and self.pacman.can_move(self.maze, self.buffered_dir):
            self.current_dir = self.buffered_dir
        if self.current_dir and self.pacman.can_move(self.maze, self.current_dir):
            self.pacman.try_move(self.maze, self.current_dir)

    def _draw(self) -> None:
        """Draws the maze background and Pac-Man, then flips the frame."""
        self.screen.blit(self.maze_surface, (0, 0))
        self.screen.blit(self.pac_img,
                         (round(self.render_x), round(self.render_y)))
        pygame.display.flip()
