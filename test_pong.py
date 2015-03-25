import pygame
from pygame.locals import *
from unittest import TestCase
from Pong import Pong

__author__ = 'ubuntu'


class TestPong(TestCase):

    def test_colisionBolaLeft(self):
        pong = Pong()
        bola = pygame.Rect(-1, 50, 10, 10)
        result = pong.colisionBola(bola,-1,1)
        self.assertEqual(result, (-1,1))

    def test_colisionBolaRight(self):
        pong = Pong()
        bola = pygame.Rect(401, 50, 10, 10)
        result = pong.colisionBola(bola,-1,1)
        self.assertEqual(result, (-1,1))

    def test_colisionBolaTop(self):
        pong = Pong()
        bola = pygame.Rect(50, 301, 10, 10)
        result = pong.colisionBola(bola,1,1)
        self.assertEqual(result, (1,-1))

    def test_colisionBolaBottom(self):
        pong = Pong()
        bola = pygame.Rect(50, -1, 10, 10)
        result = pong.colisionBola(bola,1,1)
        self.assertEqual(result, (1,-1))

    def test_colisionBolaNot(self):
        pong = Pong()
        bola = pygame.Rect(50, 50, 10, 10)
        result = pong.colisionBola(bola,1,1)
        self.assertEqual(result, (1,1))

    def test_colisionPala(self):
        pong = Pong()
        bola = pygame.Rect(60, 70, 10, 10)
        pala = pygame.Rect(50, 50, 10, 40)
        pala2 = pygame.Rect(300, 50, 10, 40)
        result = pong.colisionPala(bola, pala, pala2,-1)
        self.assertEqual(result, -1)


    def test_colisionPala2(self):
        pong = Pong()
        bola = pygame.Rect(290, 50, 10, 10)
        pala = pygame.Rect(50, 50, 10, 40)
        pala2 = pygame.Rect(300, 40, 10, 40)
        result = pong.colisionPala(bola, pala, pala2,1)
        self.assertEqual(result, -1)

    def test_colisionPalaNot(self):
        pong = Pong()
        bola = pygame.Rect(60, 40, 10, 10)
        pala = pygame.Rect(50, 50, 10, 40)
        pala2 = pygame.Rect(300, 50, 10, 40)
        result = pong.colisionPala(bola, pala, pala2,-1)
        self.assertEqual(result, 1)


