import os

import pygame

from ..entities import (PacMan, 
                        Entity, 
                        RedGhost, 
                        BlueGhost, 
                        OrangeGhost, 
                        PurpuleGhost, 
                        Pacgum)
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
GHOST_BLUE_SPRITE = "assets/ghost_blue.png"
GHOST_ORANGE_SPRITE = "assets/ghost_orange.png"
GHOST_PINK_SPRITE = "assets/ghost_pink.png"
GHOST_RED_SPRITE = "assets/ghost_red.png"

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


def find_corner(maze: list[list[int]]):
    rows, cols = len(maze), len(maze[0])
    return ([(0, 0), (0, rows - 1), (cols - 1, 0), (cols - 1, rows - 1)])


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
        self.frame_count = 0
        self.clock = pygame.time.Clock()

        self.maze_surface = draw_maze(maze)
        # self.pac_img = self._load_sprite(PAC_SPRITE)

        spawn_col, spawn_row = find_spawn(maze)
        red_pos, blue_pos, orange_pos, pink_pos = find_corner(maze)
        for y, line in enumerate(maze):
            for x, cell in enumerate(line):
                if cell != 15:
                    check_super = False
                    score = 100
                    if (
                        x in [0, len(maze[0]) - 1]
                        and y in [0, len(maze[0]) - 1]
                    ):
                        check_super = True
                        score = 200
                    Pacgum(x, y, check_super, score)
        maze_infos = (len(maze) - 1, len(maze[0]) - 1)
        self.pacman = PacMan(spawn_col, spawn_row, 
                             maze_infos=maze_infos)
        self.ghosts = [RedGhost(red_pos[0], red_pos[1],
                                self.pacman.pos, maze_infos=maze_infos),
                       BlueGhost(blue_pos[0], blue_pos[1],
                                 self.pacman.pos, maze_infos=maze_infos),
                       OrangeGhost(orange_pos[0], orange_pos[1],
                                   self.pacman.pos, maze_infos=maze_infos),
                       PurpuleGhost(pink_pos[0], pink_pos[1],
                                    self.pacman.pos, maze_infos=maze_infos)]
        self.speed = TAILLE_CASE / (MOVE_INTERVAL / 1000) - 80
        self.render_x = float(spawn_col * TAILLE_CASE)
        self.render_y = float(spawn_row * TAILLE_CASE)
        self.current_dir: str | None = None
        self.buffered_dir: str | None = None

    @staticmethod
    def _load_sprite(path: str, div: int = 1) -> pygame.Surface:
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
        dim = (TAILLE_CASE//div, TAILLE_CASE//div)
        return pygame.transform.scale(image, dim)

    def run(self) -> None:
        """Main loop: read time, read keys, move Pac-Man, draw."""
        running = True
        while running:
            self.frame_count = (self.frame_count + 1) % 10
            dt = self.clock.tick(60) / 10
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
                if event.key == pygame.K_ESCAPE:
                    return False
                self.buffered_dir = KEY_TO_DIR.get(
                    event.key, self.buffered_dir)
        return True

    def _update(self, dt: float) -> None:
        """
        Advances Pac-Man: step on the grid, then slide toward the cell.
        """
        Pacgum.check_eaten(self.pacman)
        for entity in Entity.entities:
            entity.update_entity(self.frame_count)
            entity.check_eaten()
            target_x = entity.pos.x * TAILLE_CASE
            target_y = entity.pos.y * TAILLE_CASE
            if entity.render_x == target_x and entity.render_y == target_y:
                self._step(entity)
                target_x = entity.pos.x * TAILLE_CASE
                target_y = entity.pos.y * TAILLE_CASE

            step = entity.speed * dt
            entity.render_x = _slide(entity.render_x, target_x, step)
            entity.render_y = _slide(entity.render_y, target_y, step)

    def _step(self, entity) -> None:
        """Chooses and applies the next grid move (buffered turn first)."""
        print(entity.facing)
        if entity.player and self.buffered_dir and entity.can_move(self.maze, self.buffered_dir):
            entity.facing = self.buffered_dir
        elif not entity.player:
            entity.find_target_tile()
            entity.find_short_path(self.maze, entity.target_tile)
            if entity.shortest_path:
                entity.facing = entity.shortest_path[0]
        if entity.facing and entity.can_move(self.maze, entity.facing):
            entity.try_move(self.maze, entity.facing)

    def _draw(self) -> None:
        self.screen.blit(self.maze_surface, (0, 0))
        for entity in Entity.entities:
            self.screen.blit(self._load_sprite(entity.sprite),
                             (round(entity.render_x),
                              round(entity.render_y)))
        for gums in Pacgum.pacgums.values():
            if not gums.super_pacgum:
                div = 3
            else:
                div = 2
            sprite = self._load_sprite(gums.sprite, div)
            x = gums.render_x + (TAILLE_CASE - sprite.get_width()) // 2
            y = gums.render_y + (TAILLE_CASE - sprite.get_height()) // 2
            self.screen.blit(sprite, (x, y))
        pygame.display.flip()
