from pos import Pos
from typing import List


class Pacgum:
    pacgums = []

    def __init__(self, pos_x: int, pos_y: int, color: List[int],
                 size: int, super_pacgum: bool, score: int):
        """
        pos_x -> col of the pacgum
        pos_y -> line of the pacgum
        color -> color of the pacgum [r,g,b]
        size -> size of the pacgum
        super_pacgum -> if true -> super else not
        """
        self.pos = Pos(pos_x, pos_y)
        self.color = color
        self.size = size
        self.super_pacgum = super_pacgum
        self.score = score
        Pacgum.pacgums.append(self)

    def is_eaten(self, hunter) -> bool:
        if not hunter.player:
            return (False)
        else:
            hunter.score += self.score
            if self.super_pacgum:
                hunter.swich_mode_all()
            return (True)
