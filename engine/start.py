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
from ball import Ball
from color import Color

def start_zmq_server(state):
    print("Starting zmq server...")
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:8080") 

    while True:
        #  Wait for next request from client
        topic = 42
        messagedata=state.toString()
        socket.send_string("%d %s" % (topic, messagedata))
        #  Do some 'work'
        time.sleep(0.1)

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
            output += obj.toString() + ","
        return output

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
    state = GameState([pad1, pad2, ball])

    FPS = 30
    fpsClock = pygame.time.Clock()

    AI_SPEED = 5

    PLAYER_SCORE = '0'
    AI_SCORE = '0'
    fontObj = pygame.font.Font('freesansbold.ttf', 64)  

    pygame.key.set_repeat(50, 25)
    x = threading.Thread(target=start_zmq_server, args=(state,), daemon=True)
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
        
        if ball.did_hit_top():
            ball.reset()
            PLAYER_SCORE = str(int(PLAYER_SCORE) + 1)

        if ball.did_hit_bottom():
            ball.reset()
            AI_SCORE = str(int(AI_SCORE) + 1)
# rearted AI
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
        ball.paint(main_window)

        main_window.blit(ball.ball, ball_rect)

        pygame.display.update()

        fpsClock.tick(FPS)
