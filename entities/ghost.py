from entity import Entity


class Ghost(Entity):
    def __init__(self, pos_x, pos_y,
                 hp=1, targetable=False):
        super().__init__(pos_x, pos_y, hp, targetable,
                         speed=1, player=False, size=8)

    def run_away(self):
        pass
    
    def find_tile(self):
        pass

#    def go_to_tile(self):
#       donne une coord target et trouve le plus court chemin pour y aller (main djiksttra/a*)

class RedGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

#    def find_path(self):
#       Sa cible est toujours la case exacte où se trouve Pac-Man

class BlueGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

#    def find_path(self):
#       Son ciblage dépend à la fois de la position de Rouge et de Pac-Man,

class OrangeGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

#    def find_path(self):
#       Si Pac-Man est loin, il cible le coin inférieur gauche du labyrinthe.
#       S'il s'approche trop de Pac-Man, il fuit vers son coin d'origine

class PurpuleGhost(Ghost):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

#    def find_path(self):
#       Il cible 4 cases devant la direction que regarde Pac-Man