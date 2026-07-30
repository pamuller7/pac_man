from .entity import Entity
from time import time


class PacMan(Entity):
    def __init__(self, pos_x, pos_y,maze_infos, hp=3, targetable=True):
        super().__init__(pos_x, pos_y, hp, targetable, maze_infos,
                         speed=3, player=True, size=8)
        self.score = 0
        self.god_mod = False
        self.chase_swich = time()
        self.assets = {
            "N": ["assets/pac_man/up/up_1.png", 
                  "assets/pac_man/up/up_2.png"],
            "S": ["assets/pac_man/down/down_1.png", 
                  "assets/pac_man/down/down_2.png"],
            "W": ["assets/pac_man/left/left_1.png", 
                  "assets/pac_man/left/left_2.png"],
            "E": ["assets/pac_man/right/right_1.png", 
                  "assets/pac_man/right/right_2.png"],
        }

    def update_entity(self, frame_count):
        if frame_count == 0:
            self.tick = (self.tick + 1) % 2
        self.sprite = self.assets[self.facing][self.tick]
        if self.god_mod:
            return
        if not self.targetable:
            if time() - self.chase_swich > self.super_duration:
                self.swich_mode()
        if self.hp <= 0:
            print("GAME OVER")

    def is_eaten(self, hunter: "Entity") -> bool:
        if super().is_eaten(hunter):
            self.chase_swich = time()
