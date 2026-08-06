from .pos import Pos
from ..error import DirectionError
from typing import List, Tuple, Any, Dict
from collections import deque
import math
from time import time
from ..renderer import CELL_SIZE


CODE_DIR = {"N": 1, "E": 2, "S": 4, "W": 8}
DELTA_DIR = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


class Entity:
    """Base class for any movable game entity (Pac-Man, ghosts)."""

    entities: List["Entity"] = []

    def __init__(self, pos_x: int, pos_y: int, hp: int,
                 targetable: bool, maze_infos: Tuple[int, int],
                 speed: float = 2.0, player: bool = False,
                 facing: str = "N") -> None:
        """Initializes a new entity and registers it globally.
        pos_x, pos_y: pos of the created item
        hp: current hp
        targetable: bool, says if the entity can be killed
        maze_infos: (max x, max y) cell of the maze.
        speed: the speed of each movable entity
        player: tells if the entity is playable or a bot
        facing: the current dir entity is facing

        once created, appends the entity in self.entities
        """
        self.pos = Pos(pos_x, pos_y)
        self.hp = hp
        self.speed = speed
        self.player = player
        self.facing = facing
        self.maze_infos = maze_infos
        self.targetable = targetable

        self.init_pos = (pos_x, pos_y)
        self.target_tile = (pos_x, pos_y)
        self.render_x = float(pos_x * 40)
        self.render_y = float(pos_y * 40)

        self.god_mod = False
        self.normal_behaviour = True
        self.alive = True

        self.score = 200
        self.respawn_time = 5
        self.super_duration = 5
        self.dead_since = 0.0
        self.chase_swich = time()
        self.tick = 0
        self.shortest_path = ""
        self.sprite = ""

        self.entities.append(self)

    def set_init_pos(self, pos_x: int, pos_y: int,
                     maze_infos: Tuple[int, int]) -> None:
        self.pos.set(pos_x, pos_y)      # mute l'objet existant
        self.init_pos = (pos_x, pos_y)
        self.maze_infos = maze_infos
        self.render_x = pos_x * CELL_SIZE
        self.render_y = pos_y * CELL_SIZE

    def get_pos(self) -> Tuple[int, int]:
        """Returns the entity's current position as (x, y)."""
        return (self.pos.x, self.pos.y)

    def moove_up(self) -> None:
        """Moves the entity up"""
        self.pos.up(1)

    def moove_down(self) -> None:
        """Moves the entity down"""
        self.pos.down(1)

    def moove_left(self) -> None:
        """Moves the entity left"""
        self.pos.left(1)

    def moove_right(self) -> None:
        """Moves the entity right"""
        self.pos.right(1)

    def can_move(self, maze: List[List[int]], direction: str) -> bool:
        """Checks if moving in `direction` is possible (no wall, in bounds).

        Raises:
            DirectionError: if `direction` is not one of 'N', 'E', 'S', 'W'.
        """
        if direction not in DELTA_DIR:
            raise DirectionError(direction)
        x, y = self.get_pos()
        dx, dy = DELTA_DIR[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= ny < len(maze) and 0 <= nx < len(maze[0])):
            return False
        return (maze[y][x] & CODE_DIR[direction]) == 0

    def try_move(self, maze: List[List[int]], direction: str) -> bool:
        """
        Moves the entity
        in `direction` if there is no wall.
        Returns True if moved.
        """
        if not self.can_move(maze, direction):
            return False
        if direction == "N":
            self.moove_up()
        elif direction == "S":
            self.moove_down()
        elif direction == "E":
            self.moove_right()
        elif direction == "W":
            self.moove_left()
        self.facing = direction
        return True

    def is_eaten(self, hunter: "Entity") -> bool:
        """
        Checks the state of the entity. if eatable, looses 1 hp
        """
        if self.player and self.god_mod:
            return False
        if not (self.alive and hunter.alive):
            return False
        if hunter.player and not self.player:
            if hunter.eats_everything:
                if not self.targetable:
                    return False
            else:
                return False
        elif self.player and not hunter.player:
            if self.eats_everything:
                if hunter.targetable:
                    return False
        else:
            return False
        if self.targetable:
            if self.player:
                x, y = self.init_pos
                self.set_init_pos(x, y, self.maze_infos)
            self.hp -= 1
            hunter.score += self.score
            self.targetable = False
            if self.hp <= 0:
                self.alive = False
                self.dead_since = time()
            return True
        return (False)

    def update_entity(self, frame_count: int) -> None:
        """Refreshes the entity for this frame (sprite, timers, state).

        Every kind of entity overrides it; the base entity does nothing.
        """
        pass

    def find_target_tile(self, avb_cells: List[Tuple[int, int]]) -> None:
        """Chooses the cell the entity walks toward.

        Only the entities driven by the game (the ghosts) override it;
        Pac-Man is driven by the player and keeps its spawn tile.
        """
        pass

    def swich_mode(self) -> None:
        """Toggles this entity's targetable state."""
        self.targetable = not self.targetable
        self.eats_everything = False
        self.chase_swich = time()

    def find_short_path(self, maze: List[List[int]],
                        target: Tuple[int, int]) -> None:
        """Computes the shortest path (BFS) from this entity to target.

        The result is stored in `self.shortest_path`: the letters of the
        directions to follow, or False when the target cannot be reached.
        """
        moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
                 (0, 1, 4, 'S'), (-1, 0, 8, 'W')]
        start = self.get_pos()
        goal = target
        height = len(maze)
        width = len(maze[0])
        prev: Dict[Tuple[int, int], Any] = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code, letter in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < width and 0 <= ny < height
                        and (maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y), letter)
                    queue.append((nx, ny))
        if goal not in prev:
            self.shortest_path = ""
            return
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        self.shortest_path = ''.join(reversed(letters))

    @classmethod
    def pac_man_hunting(cls) -> None:
        """Makes Pac-Man the hunter: only the ghosts stay targetable."""
        for entity in cls.entities:
            if entity.player:
                entity.eats_everything = True
                entity.targetable = True
            else:
                entity.targetable = True
            entity.chase_swich = time()

    @classmethod
    def swich_mode_all(cls) -> None:
        """Toggles targetable state for every registered entity."""
        for entity in cls.entities:
            entity.swich_mode()

    @classmethod
    def reset_all(cls) -> None:
        """Clears the global entity registry (new game/level)."""
        cls.entities.clear()

    @staticmethod
    def get_dist(origin: Tuple[int, int],
                 target: Tuple[int, int]) -> float:
        """Returns the euclidean distance between two points."""
        x_o, y_o = origin
        x_t, y_t = target
        return math.sqrt((x_o - x_t) ** 2 + (y_o - y_t) ** 2)

    @classmethod
    def collide(cls, entity1: "Entity", entity2: "Entity") -> bool:
        if (
            abs(entity1.render_x - entity2.render_x) < CELL_SIZE//2
            and abs(entity1.render_y - entity2.render_y) < CELL_SIZE//2
        ):
            return (True)
        return (False)

    @classmethod
    def check_eaten(cls) -> None:
        """Resolves every collision between two entities on the same cell."""
        for entity1 in cls.entities:
            for entity2 in cls.entities:
                if entity1 == entity2:
                    continue
                if (cls.collide(entity1, entity2)):
                    entity1.is_eaten(entity2)
                    if not entity2.player and entity1.player:
                        entity2.normal_behaviour = False
                        entity2.chase_swich = time()
                    elif not entity1.player and entity2.player:
                        entity1.normal_behaviour = False
                        entity1.chase_swich = time()
