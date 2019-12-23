import pygame
from SpriteSheet import SpriteSheet
from Tank import Tank

class GameMap(object):
    def __char_to_tile(self, character):
        map = {
            "v": "tileSand_roadEast.png",
            "h": "tileSand_roadNorth.png",
            "q": "tileSand_roadSplitS.png",
            "r": "tileSand_roadCornerLR.png",
            "L": "tileSand_roadCornerUL.png",
            "t": "treeGreen_small.png",
            "T": "treeGreen_large.png"
        }
        return map.get(character, "")

    def __set_tile(self, x, y, character):
        if character in ("1", "2"):
            if character == "1":
                self.player1 = Tank(1, x, y, self.tile_size, "down")
            else:
                self.player2 = Tank(2, x, y, self.tile_size, "up")
        else:
            tile_name = self.__char_to_tile(character)
            if tile_name != "":
                self.map[y * self.dim + x] = tile_name

    def size(self):
        return self.dim

    def tile_to_screen(self, tile_pos):
        return tile_pos * self.tile_size

    def __init__(self, map_file, dimension, tile_size):
        self.player1 = None
        self.player2 = None
        self.tile_size = tile_size
        self.dim = dimension
        dd = dimension * dimension
        self.map = [""] * dd
        with open(map_file) as fp:
            for l in range(dimension):
                line = fp.readline()
                for c in range(dimension):
                    self.__set_tile(c, l, line[c])

    def get_initial_tank_state(self, player):
        if player == 1:
            return self.player1
        else:
            return self.player2

    def unset(self, value):
        for v in value:
            return v

    def blit(self, screen, sheet, pos_x, pos_y):
        tile = self.map[pos_y * self.dim + pos_x]
        if tile != "":
            x = self.tile_to_screen(pos_x)
            y = self.tile_to_screen(pos_y)
            screen.blit(sheet.get_image_name(tile),(x,y))

