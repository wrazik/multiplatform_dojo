import pygame
from SpriteSheet import SpriteSheet
from GameMap import GameMap
from Tank import Tank
from Controller import Controller, DummyController
from Animation import Animation, Move, Rotate, Idle


class Player(object):
    def __init__(self, initial_tank_state, image, tile_size, controller):
        self.state = initial_tank_state
        self.controller = controller
        self.image = image
        self.tile_size = tile_size
        self.animation = Idle(self.tile_size, self.state.orientation())

    def string_to_animation(self, name):
        orientation = self.state.orientation()
        return {
            "left": Rotate(self.tile_size, orientation, "left"),
            "right": Rotate(self.tile_size, orientation, "right"),
            "forward": Move(self.tile_size, orientation, "forward"),
            "backward": Move(self.tile_size, orientation, "backward"),
        }.get(name, Idle(self.tile_size, orientation))
        # TODO: Add Fire animation

    def set_animation(self, animation):
        self.animation = animation

    def step(self, delta_ms):
        if self.animation.done():
            self.state.set_orientation(self.animation.post_orientation())
            self.state.update_pos_x(self.animation.post_off_x())
            self.state.update_pos_y(self.animation.post_off_y())
            self.animation = self.string_to_animation(self.controller.next())
        self.animation.step(delta_ms)

    def canvas_image(self):
        return self.image

    def canvas_x(self):
        return self.state.canvas_x() + self.animation.offset_x()

    def canvas_y(self):
        return self.state.canvas_y() + self.animation.offset_y()

    def angle(self):
        return {
            "up": 180,
            "down": 0,
            "left": 270,
            "right": 90
        }.get(self.state.orientation(), 0) + self.animation.angle()


class Preview(object):
    def __init__(self):
        self.tile_size = 64
        self.map_dim = 16
        self.map_size = self.tile_size * self.map_dim
        self.screen = pygame.display.set_mode((self.map_size,self.map_size))
        self.sheet = SpriteSheet("allSprites_default.png", "allSprites_default.xml")
        self.map = GameMap("map.txt", self.map_dim, self.tile_size)
        self.players = []
        self.init_tanks()

    def init_tanks(self):
        for t in range(4):
            tank = self.map.get_initial_tank_state(t + 1)
            if tank is None:
                break
            image = self.sheet.get_image_name(tank.image_name())
            player = Player(tank, image, self.tile_size, DummyController())
            player.set_animation(Move(self.tile_size, "up", "forward"))
            self.players.append(player)

    def render_sand(self):
        base_tile = "tileSand1.png"
        for y in range(self.map_dim):
            off_y = y * self.tile_size
            for x in range(self.map_dim):
                off_x = x * self.tile_size
                self.screen.blit(self.sheet.get_image_name(base_tile),(off_x,off_y))

    def render_obstacles(self):
        for y in range(self.map_dim):
            for x in range(self.map_dim):
                self.map.blit(self.screen, self.sheet, x, y)

    def render_tanks(self, delta_ms):
        for player in self.players:
            player.step(delta_ms)
            angle = player.angle()
            image = pygame.transform.rotate(player.canvas_image(), angle)
            pos = (player.canvas_x(),player.canvas_y())
            self.screen.blit(image,pos)

    def render(self, delta_ms):
        self.render_sand()
        self.render_obstacles()
        self.render_tanks(delta_ms)

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Tanks!")

    preview = Preview()
    preview.render(0)

    pygame.display.flip()

    running = True
    last_frame = 0
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        this_frame = pygame.time.get_ticks()
        if last_frame == 0:
            pass
        else:
            delta = this_frame - last_frame
            preview.render(delta)
            pygame.display.flip()
        foo = clock.tick(30)

        last_frame = this_frame

if __name__=="__main__":
    main()


