from pos import Pos
from typing import List


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
        Entity.entities.append(self)

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
            return (True)
        return (False)

    def swich_mode(self):
        self.targetable = not self.targetable

    def swich_mode_all():
        for entity in Entity.entities:
            entity.swich_mode()
