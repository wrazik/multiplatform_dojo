#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import sockets
import threading
import zmq
import time

from pygame.locals import *
from enum import Enum
from pad import Pad

class Color:
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    LT_BLUE = (230, 255, 255)

def start_zmq_server():
    print("Starting zmq server...")
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:8080") 

    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(1)

        print("Waiting...")

def print_points1(fontObj, main_window):
    text1 = fontObj.render(PLAYER_SCORE, True, (0, 0, 0))
    text_player_rect = text1.get_rect()
    text_player_rect.center = (WIDTH / 2, HEIGHT * 0.75)
    main_window.blit(text1, text_player_rect)

def print_pointsAI(fontObj, main_window):
    textAI = fontObj.render(AI_SCORE, True, (0, 0, 0))
    text_ai_rect = textAI.get_rect()
    text_ai_rect.center = (WIDTH / 2, HEIGHT / 4)
    main_window.blit(textAI, text_ai_rect)

class GameState:
    def __init__(self, objects):
        self.objects = objects

    def toString(self):
        output = ""
        for obj in self.objects:
            output += obj + ","

class Ball:
    def __init__(self, pygame):
        WIDTH = 800
        HEIGHT = 400
        
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

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y(self):
        self.y_speed *= -1

if __name__== "__main__":
    # inicjacja modułu pygame
    pygame.init()

    WIDTH = 800
    HEIGHT = 400
    main_window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Prosty Pong')

    pad1 = Pad(pygame, Color.BLUE, 350, 360)
    pad2 = Pad(pygame, Color.RED, 350, 20)
    ball = Ball(pygame)

    FPS = 30
    fpsClock = pygame.time.Clock()

    AI_SPEED = 5

    PLAYER_SCORE = '0'
    AI_SCORE = '0'
    fontObj = pygame.font.Font('freesansbold.ttf', 64)  

    pygame.key.set_repeat(50, 25)
    x = threading.Thread(target=start_zmq_server, daemon=True)
    x.start()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pad1.left()
                if event.key == pygame.K_RIGHT:
                    pad1.right()
        

        
        ball.update_pos()
        ball_rect = ball.ball_rect

        if ball_rect.right >= WIDTH:
            ball.bounce_x()
        if ball_rect.left <= 0:
            ball.bounce_x()

        if ball_rect.top <= 0: 
            ball_rect.x = WIDTH / 2 
            ball_rect.y = HEIGHT / 2
            PLAYER_SCORE = str(int(PLAYER_SCORE) + 1)

        if ball_rect.bottom >= HEIGHT: 
            ball_rect.x = WIDTH / 2
            ball_rect.y = HEIGHT / 2
            AI_SCORE = str(int(AI_SCORE) + 1)

        if ball_rect.centerx > pad2.rect.centerx:
            pad2.rect.x += AI_SPEED
        elif ball_rect.centerx < pad2.rect.centerx:
            pad2.rect.x -= AI_SPEED

        if ball_rect.colliderect(pad2.rect):
            ball.bounce_y();
            ball_rect.top = pad2.rect.bottom

        if ball_rect.colliderect(pad1.rect):
            ball.bounce_y();
            ball_rect.bottom = pad1.rect.top

        main_window.fill(Color.LT_BLUE) 

        print_points1(fontObj, main_window)
        print_pointsAI(fontObj, main_window)

        pad1.paint(main_window)
        pad2.paint(main_window)

        main_window.blit(ball.ball, ball_rect)

        pygame.display.update()

        fpsClock.tick(FPS)
