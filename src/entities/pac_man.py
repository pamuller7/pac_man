from .entity import Entity
from time import time

class PacMan(Entity):
    def __init__(self, pos_x, pos_y, sprite, hp=3, targetable=True):
        super().__init__(pos_x, pos_y, hp, targetable, sprite,
                         speed=3, player=True, size=8)
        self.score = 0
        self.invisibility_time = 5
        self.god_mod = False
        self.chase_swich = time()

    def update_entity(self):
        if self.god_mod:
            return
        if not self.targetable:
            if time() - self.chase_swich > self.invisibility_time:
                self.chase_swich = time()
                self.targetable = True
        if self.hp <= 0:
            print("GAME OVER")

    def is_eaten(self, hunter: "Entity") -> bool:
        if super().is_eaten(hunter):
            self.chase_swich = time()
