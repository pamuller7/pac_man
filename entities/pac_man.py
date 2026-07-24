from entity import Entity


class PacMan(Entity):
    def __init__(self, pos_x, pos_y, hp=3, targetable=True):
        super().__init__(pos_x, pos_y, hp, targetable,
                         speed=1, player=True, size=8)
        self.score = 0