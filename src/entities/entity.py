from .pos import Pos
from ..error import DirectionError
from typing import List, Tuple
from collections import deque
import math
from time import time


CODE_DIR = {"N": 1, "E": 2, "S": 4, "W": 8}
DELTA_DIR = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

class Entity:
    """Base class for any movable game entity (Pac-Man, ghosts)."""

    entities: List["Entity"] = []

    def __init__(self, pos_x: int, pos_y: int, hp: int,
                 targetable: bool, sprite: str, speed: int = 2,
                 player: bool = False, size: int = 8, facing="N") -> None:
        """Initializes a new entity and registers it globally."""
        self.pos = Pos(pos_x, pos_y)
        self.init_pos = (pos_x, pos_y)
        self.hp = hp
        self.targetable = targetable
        self.speed = speed
        self.player = player
        self.size = size
        self.facing = facing
        self.alive = True
        self.speed = speed
        self.shortest_path: str | bool = False
        self.sprite = sprite
        self.render_x = float(pos_x * 40)
        self.render_y = float(pos_y * 40)
        self.entities.append(self)

    def get_pos(self) -> Tuple[int, int]:
        """Returns the entity's current position as (x, y)."""
        return (self.pos.x, self.pos.y)

    def moove_up(self) -> None:
        """Moves the entity up by its speed."""
        self.pos.up(1)

    def moove_down(self) -> None:
        """Moves the entity down by its speed."""
        self.pos.down(1)

    def moove_left(self) -> None:
        """Moves the entity left by its speed."""
        self.pos.left(1)

    def moove_right(self) -> None:
        """Moves the entity right by its speed."""
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
        """Moves the entity in `direction` if there is no wall. Returns True if moved."""
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

    @classmethod
    def check_eaten(cls):
        for entity1 in cls.entities:
            for entity2 in cls.entities:
                if entity1 == entity2:
                    continue
                if entity1.pos.get_pos() == entity2.pos.get_pos():
                    entity1.is_eaten(entity2)

    def is_eaten(self, hunter: "Entity") -> bool:
        """Checks if this entity is eaten by the hunter entity."""
        if self.targetable and not hunter.targetable:
            self.hp -= 1
            self.targetable = False
            print("HERE")
            hunter.switch_state()
            if self.hp <= 0:
                self.alive = False
            return True
        return False

    def swich_mode(self) -> None:
        """Toggles this entity's targetable state."""
        self.targetable = not self.targetable

    @staticmethod
    def swich_mode_all() -> None:
        """Toggles targetable state for every registered entity."""
        for entity in Entity.entities:
            entity.swich_mode()

    @staticmethod
    def reset_all() -> None:
        """Clears the global entity registry (new game/level)."""
        Entity.entities.clear()

    def find_short_path(self, maze: List[List[int]],
                        target: Tuple[int, int]) -> None:
        """Computes the shortest path (BFS) from this entity to target."""
        moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
                 (0, 1, 4, 'S'), (-1, 0, 8, 'W')]
        start = self.get_pos()
        goal = target
        height = len(maze)
        width = len(maze[0])
        prev: dict = {start: None}
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
            self.shortest_path = False
            return
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        self.shortest_path = ''.join(reversed(letters))

    @staticmethod
    def get_dist(origin: Tuple[int, int],
                 target: Tuple[int, int]) -> float:
        """Returns the euclidean distance between two points."""
        x_o, y_o = origin
        x_t, y_t = target
        return math.sqrt((x_o - x_t) ** 2 + (y_o - y_t) ** 2)
