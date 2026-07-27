from pos import Pos
from typing import List, Tuple
from collections import deque
import math


class Entity:
    """Base class for any movable game entity (Pac-Man, ghosts)."""

    entities: List["Entity"] = []

    def __init__(self, pos_x: int, pos_y: int, hp: int,
                 targetable: bool, speed: int = 1,
                 player: bool = False, size: int = 8) -> None:
        """Initializes a new entity and registers it globally."""
        self.pos = Pos(pos_x, pos_y)
        self.init_pos = (pos_x, pos_y)
        self.hp = hp
        self.targetable = targetable
        self.speed = speed
        self.player = player
        self.size = size
        self.alive = True
        self.shortest_path: str | bool = False
        Entity.entities.append(self)

    def get_pos(self) -> Tuple[int, int]:
        """Returns the entity's current position as (x, y)."""
        return (self.pos.x, self.pos.y)

    def moove_up(self) -> None:
        """Moves the entity up by its speed."""
        self.pos.up(self.speed)

    def moove_down(self) -> None:
        """Moves the entity down by its speed."""
        self.pos.down(self.speed)

    def moove_left(self) -> None:
        """Moves the entity left by its speed."""
        self.pos.left(self.speed)

    def moove_right(self) -> None:
        """Moves the entity right by its speed."""
        self.pos.right(self.speed)

    def is_eaten(self, hunter: "Entity") -> bool:
        """Checks if this entity is eaten by the hunter entity."""
        if self.targetable and not hunter.targetable:
            self.hp -= 1
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