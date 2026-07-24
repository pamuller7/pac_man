from pos import Pos
from typing import List, Tuple
from collections import deque



class Entity:
    entities: List["Entity"] = []

    def __init__(self, pos_x: int, pos_y: int, hp: int,
                 targetable: bool, speed: int = 1,
                 player: bool = False, size: int = 8):
        self.pos = Pos(pos_x, pos_y)
        self.hp = hp
        self.targetable = targetable
        self.speed = speed
        self.player = player
        self.size = size
        self.alive = True
        self._shortest_path = False
        Entity.entities.append(self)
    
    def get_pos(self):
        return (self.pos.x, self.pos.y)

    def moove_up(self):
        self.pos.up(self.speed)

    def moove_down(self):
        self.pos.down(self.speed)

    def moove_left(self):
        self.pos.left(self.speed)

    def moove_right(self):
        self.pos.right(self.speed)

    def is_eaten(self, hunter) -> bool:
        if self.targetable and not hunter.targetable:
            self.hp -= 1
            if self.hp == 0:
                self.alive = False
            return (True)
        return (False)

    def swich_mode(self):
        self.targetable = not self.targetable

    def swich_mode_all():
        for entity in Entity.entities:
            entity.swich_mode()

    def find_short_path(self, target: Tuple[int, int]) -> None:
        # BFS: shortest entry->exit path in O(cells).
        moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
                 (0, 1, 4, 'S'), (-1, 0, 8, 'W')]   # dx, dy, wall code, letter
        start = self.get_pos()
        goal = target
        prev: dict = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code, letter in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self._width and 0 <= ny < self._height
                        and (self._maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y), letter)
                    queue.append((nx, ny))
        if goal not in prev:
            self._shortest_path = False
            print("Error: no shortest path found.")
            return
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        self._shortest_path = ''.join(reversed(letters))
        return
