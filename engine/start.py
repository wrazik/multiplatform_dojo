#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *

# inicjacja modułu pygame
pygame.init()

# szerokość i wysokość okna gry
WIDTH = 800
HEIGHT = 400
# kolor okna gry, składowe RGB zapisane w tupli
LT_BLUE = (230, 255, 255)

# powierzchnia do rysowania, czyli inicjacja okna gry
main_window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# tytuł okna gry
pygame.display.set_caption('Prosty Pong')

# pad gracza #########################################################
PAD_WIDTH = 100  # szerokość
PAD_HEIGHT = 20  # wysokość
BLUE = (0, 0, 255)  # kolor paletki
PAD1_POS = (350, 360)  # początkowa pozycja zapisana w tupli
# utworzenie powierzchni paletki, wypełnienie jej kolorem,
pad1 = pygame.Surface([PAD_WIDTH, PAD_HEIGHT])
pad1.fill(BLUE)
# ustawienie prostokąta zawierającego paletkę w początkowej pozycji
pad1_rect = pad1.get_rect()
pad1_rect.x = PAD1_POS[0]
pad1_rect.y = PAD1_POS[1]

# piłka #################################################################
BALL_WIDTH = 20  # szerokość
BALL_HEIGHT = 20  # wysokość
BALL_X_SPEED = 4  # prędkość pozioma x
BALL_Y_SPEED = 4  # prędkość pionowa y
GREEN = (0, 255, 0)  # kolor piłki
# utworzenie powierzchni piłki, narysowanie piłki i wypełnienie kolorem
pilka = pygame.Surface([BALL_WIDTH, BALL_HEIGHT], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(pilka, GREEN, [0, 0, BALL_WIDTH, BALL_HEIGHT])
# ustawienie prostokąta zawierającego piłkę w początkowej pozycji
ball_rect = pilka.get_rect()
ball_rect.x = WIDTH / 2
ball_rect.y = HEIGHT / 2

# ustawienia animacji ###################################################
FPS = 30  # liczba klatek na sekundę
fpsClock = pygame.time.Clock()  # zegar śledzący czas

# pad ai ############################################################
RED = (255, 0, 0)
PALETKA_AI_POZ = (350, 20)  # początkowa pozycja zapisana w tupli
# utworzenie powierzchni paletki, wypełnienie jej kolorem,
padAI = pygame.Surface([PAD_WIDTH, PAD_HEIGHT])
padAI.fill(RED)
# ustawienie prostokąta zawierającego paletkę w początkowej pozycji
padAI_prost = padAI.get_rect()
padAI_prost.x = PALETKA_AI_POZ[0]
padAI_prost.y = PALETKA_AI_POZ[1]
# szybkość paletki AI
AI_SPEED = 5

# komunikaty tekstowe ###################################################
# zmienne przechowujące punkty i funkcje wyświetlające punkty
PKT_1 = '0'
PKT_AI = '0'
fontObj = pygame.font.Font('freesansbold.ttf', 64)  # czcionka komunikatów


def print_points1():
    tekst1 = fontObj.render(PKT_1, True, (0, 0, 0))
    tekst_prost1 = tekst1.get_rect()
    tekst_prost1.center = (WIDTH / 2, HEIGHT * 0.75)
    main_window.blit(tekst1, tekst_prost1)


def print_pointsAI():
    tekstAI = fontObj.render(PKT_AI, True, (0, 0, 0))
    tekst_prostAI = tekstAI.get_rect()
    tekst_prostAI.center = (WIDTH / 2, HEIGHT / 4)
    main_window.blit(tekstAI, tekst_prostAI)

# powtarzalność klawiszy (delay, interval)
pygame.key.set_repeat(50, 25)

# pętla główna programu
while True:
    # obsługa zdarzeń generowanych przez gracza
    for event in pygame.event.get():
        # przechwyć zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # przechwyć ruch myszy
        if event.type == MOUSEMOTION:
            myszaX, myszaY = event.pos  # współrzędne x, y kursora myszy

            # oblicz przesunięcie paletki gracza
            przesuniecie = myszaX - (PAD_WIDTH / 2)

            # jeżeli wykraczamy poza okno gry w prawo
            if przesuniecie > WIDTH - PAD_WIDTH:
                przesuniecie = WIDTH - PAD_WIDTH
            # jeżeli wykraczamy poza okno gry w lewo
            if przesuniecie < 0:
                przesuniecie = 0
            # zaktualizuj położenie paletki w poziomie
            pad1_rect.x = przesuniecie

        # przechwyć naciśnięcia klawiszy kursora
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pad1_rect.x -= 5
                if pad1_rect.x < 0:
                    pad1_rect.x = 0
            if event.key == pygame.K_RIGHT:
                pad1_rect.x += 5
                if pad1_rect.x > WIDTH - PAD_WIDTH:
                    pad1_rect.x = WIDTH - PAD_WIDTH

    # ruch piłki ########################################################
    # przesuń piłkę po obsłużeniu zdarzeń
    ball_rect.move_ip(BALL_X_SPEED, BALL_Y_SPEED)

    # jeżeli piłka wykracza poza pole gry
    # z lewej/prawej – odwracamy kierunek ruchu poziomego piłki
    if ball_rect.right >= WIDTH:
        BALL_X_SPEED *= -1
    if ball_rect.left <= 0:
        BALL_X_SPEED *= -1

    if ball_rect.top <= 0:  # piłka uciekła górą
        # BALL_Y_SPEED *= -1  # odwracamy kierunek ruchu pionowego piłki
        ball_rect.x = WIDTH / 2  # więc startuję ze środka
        ball_rect.y = HEIGHT / 2
        PKT_1 = str(int(PKT_1) + 1)

    if ball_rect.bottom >= HEIGHT:  # piłka uciekła dołem
        ball_rect.x = WIDTH / 2  # więc startuję ze środka
        ball_rect.y = HEIGHT / 2
        PKT_AI = str(int(PKT_AI) + 1)

    # AI (jak gra komputer)
    # jeżeli piłka ucieka na prawo, przesuń za nią paletkę
    if ball_rect.centerx > padAI_prost.centerx:
        padAI_prost.x += AI_SPEED
    # w przeciwnym wypadku przesuń w lewo
    elif ball_rect.centerx < padAI_prost.centerx:
        padAI_prost.x -= AI_SPEED

    # jeżeli piłka dotknie paletki AI, skieruj ją w przeciwną stronę
    if ball_rect.colliderect(padAI_prost):
        BALL_Y_SPEED *= -1
        # uwzględnij nachodzenie paletki na piłkę (przysłonięcie)
        ball_rect.top = padAI_prost.bottom

    # jeżeli piłka dotknie paletki gracza, skieruj ją w przeciwną stronę
    if ball_rect.colliderect(pad1_rect):
        BALL_Y_SPEED *= -1
        # zapobiegaj przysłanianiu paletki przez piłkę
        ball_rect.bottom = pad1_rect.top

    # rysowanie obiektów ################################################
    main_window.fill(LT_BLUE)  # wypełnienie okna gry kolorem

    print_points1()  # wyświetl punkty gracza
    print_pointsAI()  # wyświetl punkty AI

    # narysuj w oknie gry paletki
    main_window.blit(pad1, pad1_rect)
    main_window.blit(padAI, padAI_prost)

    # narysuj w oknie piłkę
    main_window.blit(pilka, ball_rect)

    # zaktualizuj okno i wyświetl
    pygame.display.update()

    # zaktualizuj zegar po narysowaniu obiektów
    fpsClock.tick(FPS)

# KONIEC
