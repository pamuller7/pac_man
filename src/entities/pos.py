class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.facing = "N" # N, E, S, W, decrit la direction a laquaelle il fait face (pour ghost)

    def up(self, moove: int = 1):
        self.y -= moove
        self.facing = "N"

    def down(self, moove: int = 1):
        self.y += moove
        self.facing = "S"

    def left(self, moove: int = 1):
        self.x -= moove
        self.facing = "W"

    def right(self, moove: int = 1):
        self.x += moove
        self.facing = "E"

    def get_pos(self):
        return (self.x, self.y)

    def get_facing(self):
        return (self.facing)
