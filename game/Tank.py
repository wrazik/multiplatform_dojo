# tank_blue.png width="42" height="46"
# tank_green.png width="42" height="46"
# tank_red.png width="38" height="46"

class Tank(object):
    def __init__(self, player, x, y, tile_size, orientation):
        if player == 1:
            self.image = "tank_green.png"
            self.offset_x = 11
        else:
            self.image = "tank_red.png"
            self.offset_x = 13
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.offset_y = 9
        self.orientation_value = orientation

    def pos_x(self):
        return self.x

    def pos_y(self):
        return self.y

    def canvas_x(self):
        return self.x * self.tile_size + self.offset_x

    def canvas_y(self):
        return self.y * self.tile_size + self.offset_y

    def image_name(self):
        return self.image

    def orientation(self):
        return self.orientation_value

    def set_orientation(self, orientation):
        self.orientation_value = orientation

    def update_pos_x(self, pos):
        self.pos_x = pos

    def update_pos_y(self, pos):
        self.pos_y = pos
