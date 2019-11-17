#! /usr/bin/env python3
# -*- coding: utf-8 -*-

WIDTH = 800
HEIGHT = 400

class Pad:
    w = 100
    h = 20
    surface = {}
    rect = {}

    def __init__(self, pygame, color, x, y):
        self.surface = pygame.Surface([self.w, self.h])
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def collides_with(self, obj):
        return self.rect.colliderect(obj)

    def left(self):
        self.rect.x -= 5
        if self.rect.x < 0:
            self.rect.x = 0

    def right(self):
        self.rect.x += 5
        if self.rect.x > WIDTH - self.w:
            self.rect.x = WIDTH - self.w

    def paint(self, main_window):
        main_window.blit(self.surface, self.rect)
