import os

import pygame

from src.renderer.display import JAUNE

# from src.entities import entity

from ..entities import (PacMan,
                        Entity,
                        RedGhost,
                        BlueGhost,
                        OrangeGhost,
                        PurpuleGhost,
                        Pacgum)
from ..config import Config, Level
from ..error import (
    AssetError,
    AssetNotFoundError,
    EmptyMazeError,
    InvalidCellError,
    MalformedMazeError,
    NoSpawnError,
)
from ..renderer import (TAILLE_CASE,
                        HUD_HEIGHT,
                        draw_maze,
                        draw_text,
                        pause_menu)

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


def slide(value: float, target: float, step: float) -> float:
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


def find_corner(maze: list[list[int]]) -> list[tuple[int, int]]:
    """Returns the four corner cells of the maze, ghost spawn points."""
    rows, cols = len(maze), len(maze[0])
    return ([(0, 0), (0, rows - 1), (cols - 1, 0), (cols - 1, rows - 1)])


class Engine:
    """Runs the game: window, Pac-Man sprite, input and the main loop.

    The maze background is drawn by the renderer; the engine owns everything
    that moves. The window and the maze surface can be injected by the
    caller so they survive from one game to the next.
    """

    def __init__(self, maze: list[list[int]],
                 screen: pygame.Surface | None = None,
                 maze_surface: pygame.Surface | None = None,
                 config: Config | None = None,
                 level: Level | None = None) -> None:
        """Sets up the maze surface and Pac-Man.

        Creates the window only if no `screen` is given, and rebuilds the
        maze surface only if no `maze_surface` is given, so several games
        in a row can share both instead of redoing them. `config` and
        `level` come from the configuration file; both fall back to their
        defaults so the engine stays usable on its own.

        Raises:
            MazeError: if the maze is empty, not rectangular or has bad cells.
            NoSpawnError: if the maze has no walkable spawn cell.
            AssetError: if the Pac-Man sprite cannot be loaded.
        """
        validate_maze(maze)
        Entity.reset_all()
        Pacgum.reset_all()
        self.config = config or Config()
        self.level = level or self.config.levels[0]
        self.maze = maze
        pygame.init()
        pygame.display.set_caption("ᗧ Pac-Man ᗧ")
        if screen is None:
            height = len(maze) * TAILLE_CASE + HUD_HEIGHT
            width = len(maze[0]) * TAILLE_CASE
            screen = pygame.display.set_mode((width, height))
        self.screen = screen
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        self.maze_surface = maze_surface or draw_maze(maze)
        spawn_col, spawn_row = find_spawn(maze)
        red_pos, blue_pos, orange_pos, pink_pos = find_corner(maze)
        self.spawn_pacgums(maze, self.level.pacgum)
        maze_infos = (len(maze[0]) - 1, len(maze) - 1)
        self.pacman = PacMan(spawn_col, spawn_row,
                             maze_infos=maze_infos,
                             hp=self.config.lives)
        self.ghosts = [RedGhost(red_pos[0], red_pos[1],
                                self.pacman.pos, maze_infos=maze_infos),
                       BlueGhost(blue_pos[0], blue_pos[1],
                                 self.pacman.pos, maze_infos=maze_infos),
                       OrangeGhost(orange_pos[0], orange_pos[1],
                                   self.pacman.pos, maze_infos=maze_infos),
                       PurpuleGhost(pink_pos[0], pink_pos[1],
                                    self.pacman.pos, maze_infos=maze_infos)]
        for ghost in self.ghosts:
            ghost.score = self.config.points_per_ghost
        self.buffered_dir: str | None = None
        self.skip_level = False

    def spawn_pacgums(self, maze: list[list[int]], count: int) -> None:
        """Spreads at most `count` pacgums over the walkable cells.

        The walkable corners always get a super pacgum; the remaining
        cells are picked at a regular interval so the pacgums stay spread
        over the whole maze instead of piling up on the first rows.
        """
        corners: list[tuple[int, int]] = []
        others: list[tuple[int, int]] = []
        for y, line in enumerate(maze):
            for x, cell in enumerate(line):
                if cell == 15:
                    continue
                is_corner = (x in (0, len(line) - 1)
                             and y in (0, len(maze) - 1))
                (corners if is_corner else others).append((x, y))
        left = count - len(corners)
        if left < len(others):
            step = len(others) / max(left, 1)
            others = [others[int(i * step)] for i in range(max(left, 0))]
        for x, y in corners[:count]:
            Pacgum(x, y, True, self.config.points_per_super_pacgum)
        for x, y in others:
            Pacgum(x, y, False, self.config.points_per_pacgum)

    @staticmethod
    def load_sprite(path: str, div: int = 1) -> pygame.Surface:
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

    def run(self) -> tuple[bool, int]:
        """Main loop. Returns (won, score) once the game is over.

        The engine does not show the endgame screen nor decide what comes
        next: the caller owns the menu flow. A level skipped from the
        pause menu counts as won, so the caller moves on to the next one.
        """
        running = True
        won = False
        while running:
            self.frame_count = (self.frame_count + 1) % 5
            dt = self.clock.tick(60) / 10
            running = self._handle_events()
            if self.skip_level:
                return True, self.pacman.score
            self._update(dt)
            self._draw()
            if not self.pacman.alive:
                running = False
            elif not Pacgum.pacgums:
                won = True
                running = False
        return won, self.pacman.score

    def _handle_events(self) -> bool:
        """Handles input; returns False when the window is closed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_p:
                    return self._pause()
                self.buffered_dir = KEY_TO_DIR.get(
                    event.key, self.buffered_dir)
        return True

    def _pause(self) -> bool:
        """Freezes the game on the pause screen.

        The game keeps showing behind the PAUSE text. Returns False when
        the window is closed or the player quits, True on resume and on
        skip, the skip being read by `run` right after.
        """
        pause_menu(self.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_p:
                        return True
                    if event.key == pygame.K_n:
                        return self._skip_level()
            # self.clock.tick(60)

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
                self.step(entity)
                target_x = entity.pos.x * TAILLE_CASE
                target_y = entity.pos.y * TAILLE_CASE

            step = entity.speed * dt
            entity.render_x = slide(entity.render_x, target_x, step)
            entity.render_y = slide(entity.render_y, target_y, step)

    def step(self, entity: Entity) -> None:
        """Chooses and applies the next grid move (buffered turn first)."""

        if (entity.player
                and self.buffered_dir
                and entity.can_move(self.maze, self.buffered_dir)):
            entity.facing = self.buffered_dir
        elif not entity.player:
            entity.find_target_tile()
            entity.find_short_path(self.maze, entity.target_tile)
            if entity.shortest_path:
                entity.facing = entity.shortest_path[0]
        if entity.facing and entity.can_move(self.maze, entity.facing):
            entity.try_move(self.maze, entity.facing)

    def _draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.maze_surface, (0, HUD_HEIGHT))
        for entity in Entity.entities:
            self.screen.blit(self.load_sprite(entity.sprite),
                             (round(entity.render_x),
                              round(entity.render_y + HUD_HEIGHT)))
        for gums in Pacgum.pacgums.values():
            if not gums.super_pacgum:
                div = 3
            else:
                div = 2
            sprite = self.load_sprite(gums.sprite, div)
            x = gums.render_x + (TAILLE_CASE - sprite.get_width()) // 2
            y = (gums.render_y + HUD_HEIGHT
                 + (TAILLE_CASE - sprite.get_height()) // 2)
            self.screen.blit(sprite, (x, y))
        draw_text(self.screen,
                  f"score: {self.pacman.score}, hp: {self.pacman.hp}",
                  36, (0, 0), JAUNE, centre=False)
        pygame.display.flip()

    def _skip_level(self) -> bool:
        """Leaves the pause menu and ends the level as won.

        Always returns True: the main loop keeps running for one more
        turn, just long enough for `run` to see the flag. The next level
        rebuilds its own pacgums, so the ones left here are dropped.
        """
        self.skip_level = True
        return True
