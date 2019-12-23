# These classes represent animations. Animations interpolate over time
# but also provide state update values used on animation end.

class Animation(object):
    def __init__(self, tile_size, orientation):
        self.tick = 0
        self.tile_size = tile_size
        self.orientation = orientation

    def percentage(self):
        if self.tick == 0:
            return 0.0
        if self.tick >= 1000:
            return 1.0
        return self.tick / 1000.0

    def step(self, delta):
        self.tick = self.tick + delta

    def done(self):
        return self.tick >= 1000

    def offset_x(self):
        return 0

    def offset_y(self):
        return 0

    def angle(self):
        return 0

    def post_off_x(self):
        return 0

    def post_off_y(self):
        return 0

    def post_orientation(self):
        return self.orientation


class Rotate(Animation):
    def __init__(self, tile_size, orientation, direction):
        super().__init__(tile_size, orientation)
        if direction == "left":
            self.direction = -1.0
        else: # right
            self.direction = 1.0

    def angle(self):
        return 90.0 * self.percentage() * self.direction

    def post_orientation(self):
        composite = self.orientation
        if self.direction < 0:
            composite = composite + "neg"
        return {
            "up": "right",
            "down": "left",
            "left": "up",
            "right": "down",
            "upneg": "left",
            "downneg": "right",
            "leftneg": "down",
            "rightneg": "up"
        }.get(composite, "up")


class Move(Animation):
    def __init__(self, tile_size, orientation, direction):
        super().__init__(tile_size, orientation)
        if direction == "forward":
            self.direction = -1.0
        else: # backward
            self.direction = 1.0
        self.ox = 0
        self.oy = 0
        if orientation == "up":
            self.oy = -1
        elif orientation == "down":
            self.oy = 1
        elif orientation == "left":
            self.ox = -1
        elif orientation == "right":
            self.ox = 1

    def offset_x(self):
        return self.ox * self.direction * self.percentage() * self.tile_size

    def offset_y(self):
        return self.oy * self.direction * self.percentage() * self.tile_size

    def post_off_x(self):
        return self.ox

    def post_off_x(self):
        return self.oy

class Idle(Animation):
    def __init__(self, tile_size, orientation):
        super().__init__(tile_size, orientation)

# TODO: Add Fire animation
