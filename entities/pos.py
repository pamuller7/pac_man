class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def up(self, moove: int = 1):
        self.y += moove

    def down(self, moove: int = 1):
        self.y -= moove

    def left(self, moove: int = 1):
        self.x -= moove

    def right(self, moove: int = 1):
        self.x += moove
