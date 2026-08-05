from typing import Tuple


class Pos:
    def __init__(self, x: int, y: int) -> None:
        """
        N, E, S, W, decrit la direction a laquaelle il fait face (pour ghost)
        """
        self.x = x
        self.y = y
        self.facing = "N"

    def set(self, pos_x: int, pos_y: int) -> None:
        self.x = pos_x
        self.y = pos_y

    def up(self, moove: int = 1) -> None:
        self.y -= moove
        self.facing = "N"

    def down(self, moove: int = 1) -> None:
        self.y += moove
        self.facing = "S"

    def left(self, moove: int = 1) -> None:
        self.x -= moove
        self.facing = "W"

    def right(self, moove: int = 1) -> None:
        self.x += moove
        self.facing = "E"

    def get_pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def get_facing(self) -> str:
        return (self.facing)
