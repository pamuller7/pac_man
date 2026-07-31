from .entity import Entity
from time import time


class PacMan(Entity):
    def __init__(self, pos_x, pos_y, maze_infos, hp=1, targetable=True):
        super().__init__(pos_x, pos_y, hp, targetable, maze_infos,
                         speed=2, player=True, size=8)
        self.score = 0
        self.god_mod = False
        self.eating = False
        self.chase_swich = time()
        self.assets = [
            {
                "N": ["assets/super_pac_man/up/up_1.png",
                      "assets/super_pac_man/up/up_2.png",
                      "assets/super_pac_man/up/up_3.png",
                      "assets/super_pac_man/up/up_2.png"],
                "S": ["assets/super_pac_man/down/down_1.png",
                      "assets/super_pac_man/down/down_2.png",
                      "assets/super_pac_man/down/down_3.png",
                      "assets/super_pac_man/down/down_2.png"],
                "W": ["assets/super_pac_man/left/left_1.png",
                      "assets/super_pac_man/left/left_2.png",
                      "assets/super_pac_man/left/left_3.png",
                      "assets/super_pac_man/left/left_2.png"],
                "E": ["assets/super_pac_man/right/right_1.png",
                      "assets/super_pac_man/right/right_2.png",
                      "assets/super_pac_man/right/right_3.png",
                      "assets/super_pac_man/right/right_2.png"],
                },
            {
                "N": ["assets/pac_man/up/up_1.png",
                      "assets/pac_man/up/up_2.png",
                      "assets/pac_man/up/up_3.png",
                      "assets/pac_man/up/up_2.png"],
                "S": ["assets/pac_man/down/down_1.png",
                      "assets/pac_man/down/down_2.png",
                      "assets/pac_man/down/down_3.png",
                      "assets/pac_man/down/down_2.png"],
                "W": ["assets/pac_man/left/left_1.png",
                      "assets/pac_man/left/left_2.png",
                      "assets/pac_man/left/left_3.png",
                      "assets/pac_man/left/left_2.png"],
                "E": ["assets/pac_man/right/right_1.png",
                      "assets/pac_man/right/right_2.png",
                      "assets/pac_man/right/right_3.png",
                      "assets/pac_man/right/right_2.png"],
                }
            ]
        self.current_asset = self.assets[1]

    def update_entity(self, frame_count):
        if frame_count == 0:
            self.tick = (self.tick + 1) % 4
        self.sprite = self.current_asset[self.facing][self.tick]
        if self.god_mod:
            return
        if not self.targetable:
            self.current_asset = self.assets[0]
            if time() - self.chase_swich > self.super_duration:
                self.swich_mode()
        else:
            self.current_asset = self.assets[1]
        if not self.alive:
            print("GAME OVER")
            self.isdead = True

    def is_eaten(self, hunter: "Entity") -> bool:
        if super().is_eaten(hunter):
            self.chase_swich = time()
