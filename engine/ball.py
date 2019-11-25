#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from color import Color

WIDTH = 800
HEIGHT = 400

class Ball:
    def __init__(self, pygame):
        
        self.w = 20
        self.h = 20
        self.x_speed = 4
        self.y_speed = 4
        self.ball = pygame.Surface([self.w, self.h], pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(self.ball, Color.GREEN, [0, 0, self.w, self.h])
        self.ball_rect = self.ball.get_rect()
        self.ball_rect.x = WIDTH / 2
        self.ball_rect.y = HEIGHT / 2

    def update_pos(self):
        self.ball_rect.move_ip(self.x_speed, self.y_speed)
        if self.ball_rect.right >= WIDTH or self.ball_rect.left <= 0:
            self.bounce_x()

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y(self):
        self.y_speed *= -1

    def reset(self):
        self.ball_rect.x = WIDTH / 2 
        self.ball_rect.y = HEIGHT / 2

    def did_hit_top(self):
        return self.ball_rect.top <= 0 

    def did_hit_bottom(self):
        return self.ball_rect.bottom >= HEIGHT

    def paint(self, main_window):
        main_window.blit(self.ball, self.ball_rect)

    def toString(self):
        return "ball %d %d" % (self.ball_rect.x, self.ball_rect.y)

