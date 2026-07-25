from entity import Entity
from pos import Pos


class Ghost(Entity):
    ghosts = dict()
    def __init__(self, pos_x: int, pos_y: int, pac_man_pos: Pos,
                 hp: int = 1, targetable: bool = False):
        super().__init__(pos_x, pos_y, hp, targetable,
                         speed=1, player=False, size=8)
        self.target_tile = (0, 0)
        self.mooves = [('N', 0, 1), ('S', 0, -1), ('W', -1, 0), ('E', 1, 0)]
        self.pac_man_pos = pac_man_pos

    def run_away(self):
        # baisse la vitesse de ghost, et essaie de s'eloigner de pac man
        pass

    def go_to_tile(self):
        if not self.shortest_path:
            return
        direction = self.shortest_path[0]
        if (direction == 'N'):
            self.moove_up()
        elif (direction == 'S'):
            self.moove_down()
        elif (direction == 'E'):
            self.moove_right()
        elif (direction == 'W'):
            self.moove_left()
        self.shortest_path.pop(0)


class RedGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Ghost.ghosts.update({"red": self})

    def find_target_tile(self):
        """
            Sa cible est toujours la case exacte où se trouve Pac-Man
        """
        self.target_tile = self.pac_man_pos.get_pos()

class BlueGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Ghost.ghosts.update({"blue": self})

    def find_target_tile(self):
        """
            Son ciblage dépend à la fois de la position de Rouge et de Pac-Man,
            (on va dire qu'il cible devant pac man si rouge derrier, derriere pac man sinon)
        """
        self.target_tile =  (0, 0)



class OrangeGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Ghost.ghosts.update({"orange": self})

    def find_target_tile(self):
        """
            Si Pac-Man est loin, il cible le centre du labyrinthe.
            S'il s'approche trop de Pac-Man, il fuit vers son coin d'origine
        """
        dist = self.get_dist(self.pos.get_pos(), self.pac_man_pos.get_pos())
        if dist > 20:
            self.target_tile = (0, 0)
        else:
            self.target_tile = self.init_pos


class PurpuleGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Ghost.ghosts.update({"purpule": self})

    def find_target_tile(self):
        """
            Il cible 4 cases devant la direction que regarde Pac-Man
        """
        x, y = self.pac_man_pos.get_pos()
        for facing, moove_x, moove_y in self.mooves:
            if self.pac_man_pos.get_facing() == facing:
                self.target_tile = x + moove_x * 4 , y + moove_y * 4
