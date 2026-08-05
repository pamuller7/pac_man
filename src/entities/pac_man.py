from .entity import Entity
from time import time
from typing import Tuple

UNTARGET_ASSETS = {
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
}

PAC_MAN_ASSETS = {
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


class PacMan(Entity):
    def __init__(self, pos_x: int, pos_y: int,
                 maze_infos: Tuple[int, int],
                 hp: int = 1, targetable: bool = True) -> None:
        super().__init__(pos_x=pos_x, pos_y=pos_y, hp=hp,
                         targetable=targetable, maze_infos=maze_infos,
                         speed=2, player=True)
        self.score = 0
        self.god_mod = False
        self.eats_everything = False
        self.assets = [UNTARGET_ASSETS, PAC_MAN_ASSETS]
        self.current_asset = self.assets[1]

    def update_entity(self, frame_count: int) -> None:
        if frame_count == 0:
            self.tick = (self.tick + 1) % len(self.current_asset[self.facing])
        self.sprite = self.current_asset[self.facing][self.tick]
        if not self.targetable and not self.god_mod:
            self.current_asset = self.assets[0]
            if time() - self.chase_swich > self.super_duration:
                self.swich_mode()
        elif self.god_mod:
            self.current_asset = self.assets[0]
        else:
            self.current_asset = self.assets[1]
        if not self.alive:
            self.isdead = True

    def is_eaten(self, hunter: "Entity") -> bool:
        """Same as `Entity.is_eaten`, but also restarts the super timer."""
        if not super().is_eaten(hunter):
            return False
        self.chase_swich = time()
        return True
