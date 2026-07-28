from .entity import Entity
from .pos import Pos
import random
from time import time


class Ghost(Entity):
    ghosts = dict()
    def __init__(self, pos_x: int, pos_y: int, sprite: str, pac_man_pos: Pos,
                 hp: int = 1, targetable: bool = False):
        super().__init__(pos_x, pos_y, hp, targetable, sprite,
                         speed=1, player=False, size=8)
        self.target_tile = (0, 0)
        self.mooves = [('N', 0, -1), ('S', 0, 1), ('W', -1, 0), ('E', 1, 0)]
        self.pac_man_pos = pac_man_pos
        self.chase = False
        self.chase_limit = 10
        self.chill = self.chase_limit * 3
        self.chasing_since = time()

    def run_away(self):
        # baisse la vitesse de ghost, et essaie de s'eloigner de pac man
        pass

    def go_spawn(self):
        self.target_tile = self.init_pos
        return (self.target_tile)

    def tracking(self):
        self.target_tile = self.pac_man_pos.get_pos()
        return (self.target_tile)

    def going_b4_pac_man(self):
        x, y = self.pac_man_pos.get_pos()
        for facing, moove_x, moove_y in self.mooves:
            if self.pac_man_pos.get_facing() == facing:
                new_pos_x = x + moove_x * 5
                new_pos_y = y + moove_y * 5
                if new_pos_x >= 0:
                    choose_x = min(new_pos_x, 40)
                else:
                    choose_x = max(new_pos_x, 0)
                if new_pos_y >= 0:
                    choose_y = min(new_pos_y, 40)
                else:
                    choose_y = max(new_pos_y, 0)
                self.target_tile = choose_x, choose_y
        return (self.target_tile)

    def random_dir(self):
        self.target_tile = (random.randint(0, 40), random.randint(0, 40))
        return (self.target_tile)

    def going_to_pac_man_if_far(self):
        dist = self.get_dist(self.pos.get_pos(), self.pac_man_pos.get_pos())
        if dist > 2:
            self.random_dir()
        else:
            self.tracking()
        return (self.target_tile)


class RedGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos)
        Ghost.ghosts.update({"red": self})

    def find_target_tile(self):
        """
            Sa cible est toujours la case exacte où se trouve Pac-Man
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        self.tracking()


class BlueGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos)
        Ghost.ghosts.update({"blue": self})

    def find_target_tile(self):
        """
            Son ciblage dépend à la fois de la position de Rouge et de Pac-Man,
            (on va dire qu'il cible devant pac man si rouge derrier, derriere pac man sinon)
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        self.going_to_pac_man_if_far()
        return (self.target_tile)


class OrangeGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos)
        Ghost.ghosts.update({"orange": self})

    def find_target_tile(self):
        """
            Si Pac-Man est loin, il cible le centre du labyrinthe.
            S'il s'approche trop de Pac-Man, il fuit vers son coin d'origine
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        self.going_to_pac_man_if_far()


class PurpuleGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos)
        Ghost.ghosts.update({"purpule": self})

    def find_target_tile(self):
        """
            Il cible 4 cases devant la direction que regarde Pac-Man
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        self.going_b4_pac_man()
