from .entity import Entity
from .pos import Pos
import random
from time import time

SCARED = [
    "assets/scared_ghost/scared_1.png", 
    "assets/scared_ghost/scared_2.png"]


class Ghost(Entity):
    ghosts = dict()

    def __init__(self, pos_x: int, pos_y: int, pac_man_pos: Pos, maze_infos,
                 hp: int = 1, targetable: bool = False, speed=2.7):
        super().__init__(pos_x, pos_y, hp, targetable, maze_infos,
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

    def find_target_tile(self):
        """
            Son ciblage dépend à la fois de la position de Rouge et 
            de Pac-Man,
            (on va dire qu'il cible devant 
            pac man si rouge derrier, derriere pac man sinon)
        """
        if self.hp <= 0:
            self.go_spawn()
            return
        if self.normal_behaviour and not self.targetable:
            self.nomal_proc()
        elif not self.normal_behaviour and not self.targetable:
            self.random_dir()
        else:
            self.run_away()

    def update_entity(self, frame_count):
        if self.hp <= 0 and self.pos.get_pos() == self.init_pos:
            self.hp = 1
            self.targetable = False
        if self.hp <= 0:
            print(self.hp)
            self.targetable = True
            self.sprite = self.assets["dead"]
        elif self.targetable:
            self.sprite = self.assets['swich'][self.tick]
        else:
            self.sprite = self.assets[self.facing][self.tick]
        if frame_count == 0:
            self.tick = (self.tick + 1) % 2
        if self.normal_behaviour and not self.targetable:
            if time() - self.chase_swich > self.chase_limit:
                self.switch_state()
        elif not self.normal_behaviour and not self.targetable:
            if time() - self.chase_swich > self.chill:
                self.switch_state()
        elif self.targetable:
            if time() - self.chase_swich > self.super_duration:
                self.targetable = False
        self.dist_from_pac_man = self.get_dist(self.pos.get_pos(),
                                               self.pac_man_pos.get_pos())

    def run_away(self):
        """Choisit comme cible le coin le plus loin de Pac-Man."""
        px, py = self.pac_man_pos.get_pos()
        max_x_maze, max_y_maze = self.maze_infos
        corners = [
            (0, 0),
            (max_x_maze, 0),
            (0, max_y_maze),
            (max_x_maze, max_y_maze),
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
    def __init__(self, pos_x, pos_y, pac_man_pos, maze_infos, speed=2):
        super().__init__(pos_x=pos_x,
                         pos_y=pos_y,
                         pac_man_pos=pac_man_pos,
                         maze_infos=maze_infos,
                         speed=speed)
        Ghost.ghosts.update({"red": self})
        self.assets = {
            "swich": SCARED,
            "dead": "assets/dead_ghost/dead.png",
            "N": ["assets/ghost_red/up/up_1.png", 
                  "assets/ghost_red/up/up_2.png"],
            "S": ["assets/ghost_red/down/down_1.png", 
                  "assets/ghost_red/down/down_2.png"],
            "W": ["assets/ghost_red/left/left_1.png", 
                  "assets/ghost_red/left/left_2.png"],
            "E": ["assets/ghost_red/right/right_1.png", 
                  "assets/ghost_red/right/right_2.png"],
        }

    def nomal_proc(self):
        """
            Sa cible est toujours la case exacte où se trouve Pac-Man
        """
        self.tracking()


class BlueGhost(Ghost):
    def __init__(self, pos_x, pos_y, pac_man_pos, maze_infos, speed=2):
        super().__init__(pos_x=pos_x,
                         pos_y=pos_y,
                         pac_man_pos=pac_man_pos,
                         maze_infos=maze_infos,
                         speed=speed)
        Ghost.ghosts.update({"blue": self})
        self.assets = {
            "swich": SCARED,
            "dead": "assets/dead_ghost/dead.png",
            "N": ["assets/ghost_blue/up/up_1.png", 
                  "assets/ghost_blue/up/up_2.png"],
            "S": ["assets/ghost_blue/down/down_1.png", 
                  "assets/ghost_blue/down/down_2.png"],
            "W": ["assets/ghost_blue/left/left_1.png", 
                  "assets/ghost_blue/left/left_2.png"],
            "E": ["assets/ghost_blue/right/right_1.png", 
                  "assets/ghost_blue/right/right_2.png"],
        }

    def nomal_proc(self):
        """
            Son ciblage dépend à la fois 
            de la position de Rouge et de Pac-Man,
            (on va dire qu'il cible devant pac man 
            si rouge derrier, derriere pac man sinon)
        """
        pac_x, pac_y = self.pac_man_pos.get_pos()
        red_x, red_y = self.ghosts['red'].pos.get_pos()
        if (pac_x - red_x) < 0 or (pac_y - red_y) < 0:
            self.going_b4_pac_man()
        else:
            self.going_b4_pac_man(-1)


class OrangeGhost(Ghost):
    def __init__(self, pos_x, pos_y, pac_man_pos, maze_infos, speed=2):
        super().__init__(pos_x=pos_x,
                         pos_y=pos_y,
                         pac_man_pos=pac_man_pos,
                         maze_infos=maze_infos,
                         speed=speed)
        Ghost.ghosts.update({"orange": self})
        self.assets = {
            "swich": SCARED,
            "dead": "assets/dead_ghost/dead.png",
            "N": ["assets/ghost_orange/up/up_1.png", 
                  "assets/ghost_orange/up/up_2.png"],
            "S": ["assets/ghost_orange/down/down_1.png", 
                  "assets/ghost_orange/down/down_2.png"],
            "W": ["assets/ghost_orange/left/left_1.png", 
                  "assets/ghost_orange/left/left_2.png"],
            "E": ["assets/ghost_orange/right/right_1.png", 
                  "assets/ghost_orange/right/right_2.png"],
        }

    def nomal_proc(self):
        """
            Si Pac-Man est loin, il cible le centre du labyrinthe.
            S'il s'approche trop de Pac-Man, il fuit vers son coin d'origine
        """
        if self.dist_from_pac_man > 10:
            self.target_tile = (10, 9)
        elif self.dist_from_pac_man <= 2:
            self.tracking()


class PurpuleGhost(Ghost):
    def __init__(self, pos_x, pos_y, pac_man_pos, maze_infos, speed=2):
        super().__init__(pos_x=pos_x,
                         pos_y=pos_y,
                         pac_man_pos=pac_man_pos,
                         maze_infos=maze_infos,
                         speed=speed)
        Ghost.ghosts.update({"purpule": self})
        self.assets = {
            "swich": SCARED,
            "dead": "assets/dead_ghost/dead.png",
            "N": ["assets/ghost_pink/up/up_1.png", 
                  "assets/ghost_pink/up/up_2.png"],
            "S": ["assets/ghost_pink/down/down_1.png", 
                  "assets/ghost_pink/down/down_2.png"],
            "W": ["assets/ghost_pink/left/left_1.png", 
                  "assets/ghost_pink/left/left_2.png"],
            "E": ["assets/ghost_pink/right/right_1.png", 
                  "assets/ghost_pink/right/right_2.png"],
        }

    def nomal_proc(self):
        """
            Il cible 4 cases devant la direction que regarde Pac-Man
        """
        self.going_b4_pac_man()
