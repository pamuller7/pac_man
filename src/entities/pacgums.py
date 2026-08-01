from src.entities.pac_man import PacMan

from .pos import Pos

SPRITE = ["assets/pacgums/pacgum.png"]


class Pacgum:
    pacgums: dict[tuple[int, int], 'Pacgum'] = dict()

    def __init__(self, pos_x: int, pos_y: int,
                 super_pacgum: bool, score: int):
        """
        pos_x -> col of the pacgum
        pos_y -> line of the pacgum
        color -> color of the pacgum [r,g,b]
        size -> size of the pacgum
        super_pacgum -> if true -> super else not
        """
        self.pos = Pos(pos_x, pos_y)
        self.render_x = float(pos_x * 40)
        self.render_y = float(pos_y * 40)
        self.sprite = SPRITE[0]
        self.super_pacgum = super_pacgum
        self.score = score
        Pacgum.pacgums.update({self.pos.get_pos(): self})

    @classmethod
    def reset_all(cls) -> None:
        """Clears the global pacgum registry (new game/level)."""
        cls.pacgums.clear()

    @classmethod
    def check_eaten(cls, hunter: PacMan) -> None:
        pos = hunter.pos.get_pos()
        pacgum = None
        if pos in cls.pacgums:
            pacgum = cls.pacgums.pop(pos)
        if pacgum:
            pacgum.is_eaten(hunter)

    def is_eaten(self, hunter: PacMan) -> bool:
        if not hunter.player:
            return (False)
        else:
            hunter.score += self.score
            if self.super_pacgum:
                hunter.pac_man_hunting()
            return (True)
