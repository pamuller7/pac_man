from .entity import Entity
from .pos import Pos
import random
from time import time


class Ghost(Entity):
    ghosts = dict()

    def __init__(self, pos_x: int, pos_y: int, sprite: str, pac_man_pos: Pos,
                 hp: int = 1, targetable: bool = False, speed=2.7):
        super().__init__(pos_x, pos_y, hp, targetable, sprite,
                         speed, player=False, size=8)
        self.target_tile = (0, 0)
        self.mooves = [('N', 0, -1), ('W', -1, 0), ('S', 0, 1), ('E', 1, 0)]
        self.pac_man_pos = pac_man_pos
        self.normal_behaviour = True
        self.speed = speed
        self.chase_limit = 10
        self.chill = self.chase_limit
        self.chase_swich = time()
        self.dist_from_pac_man = 0.0

    def switch_state(self):
        self.normal_behaviour = not self.normal_behaviour
        self.chase_swich = time()

    def update_entity(self):
        if self.normal_behaviour:
            if time() - self.chase_swich > self.chase_limit:
                self.switch_state()
        if not self.normal_behaviour:
            if time() - self.chase_swich > self.chill:
                self.switch_state()
        self.dist_from_pac_man = self.get_dist(self.pos.get_pos(),
                                               self.pac_man_pos.get_pos())

    def run_away(self):
        """Choisit comme cible le coin le plus loin de Pac-Man."""
        px, py = self.pac_man_pos.get_pos()
        corners = [
            (0, 0),
            (19, 0),
            (0, 19),
            (19, 19),
        ]
        self.target_tile = max(
            corners,
            key=lambda corner: self.get_dist(corner, (px, py))
        )
        return self.target_tile

    def go_spawn(self):
        self.target_tile = self.init_pos
        return (self.target_tile)

    def tracking(self):
        self.target_tile = self.pac_man_pos.get_pos()
        return (self.target_tile)

    def going_b4_pac_man(self, sign=1):
        x, y = self.pac_man_pos.get_pos()
        for facing, moove_x, moove_y in self.mooves:
            if self.pac_man_pos.get_facing() == facing:
                new_pos_x = x + sign * moove_x * 4
                new_pos_y = y + sign * moove_y * 4
                if new_pos_x >= 0:
                    choose_x = min(new_pos_x, 19)
                else:
                    choose_x = max(new_pos_x, 0)
                if new_pos_y >= 0:
                    choose_y = min(new_pos_y, 19)
                else:
                    choose_y = max(new_pos_y, 0)
                self.target_tile = choose_x, choose_y
        return (self.target_tile)

    def random_dir(self):
        self.target_tile = (random.randint(0, 19), random.randint(0, 19))
        return (self.target_tile)


class RedGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos, speed=2):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos, speed)
        Ghost.ghosts.update({"red": self})

    def find_target_tile(self):
        """
            Sa cible est toujours la case exacte où se trouve Pac-Man
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        if self.normal_behaviour:
            self.tracking()
        else:
            self.random_dir()


class BlueGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos, speed=2):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos, speed)
        Ghost.ghosts.update({"blue": self})

    def find_target_tile(self):
        """
            Son ciblage dépend à la fois de la position de Rouge et de Pac-Man,
            (on va dire qu'il cible devant pac man si rouge derrier, derriere pac man sinon)
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        if self.normal_behaviour:
            pac_x, pac_y = self.pac_man_pos.get_pos()
            red_x, red_y = self.ghosts['red'].pos.get_pos()
            if (pac_x - red_x) < 0 or (pac_y - red_y) < 0:
                self.going_b4_pac_man()
            else:
                self.going_b4_pac_man(-1)
        else:
            self.random_dir()


class OrangeGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos, speed=2):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos, speed)
        Ghost.ghosts.update({"orange": self})

    def find_target_tile(self):
        """
            Si Pac-Man est loin, il cible le centre du labyrinthe.
            S'il s'approche trop de Pac-Man, il fuit vers son coin d'origine
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        if self.normal_behaviour:
            if self.dist_from_pac_man > 10:
                self.target_tile = (10, 9)
            elif self.dist_from_pac_man <= 2:
                self.tracking()
            else:
                self.run_away()
        else:
            self.random_dir()


class PurpuleGhost(Ghost):
    def __init__(self, pos_x, pos_y, sprite, pac_man_pos, speed=2):
        super().__init__(pos_x, pos_y, sprite, pac_man_pos, speed)
        Ghost.ghosts.update({"purpule": self})

    def find_target_tile(self):
        """
            Il cible 4 cases devant la direction que regarde Pac-Man
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        self.going_b4_pac_man()
