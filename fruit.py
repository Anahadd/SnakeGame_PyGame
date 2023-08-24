import pygame
from pygame.locals import *
import random

rW = 906
rH = 608
screen = pygame.display.set_mode((rW, rH))

class Fruits:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 32, 32)
        self.count = 0

    def drawFruit(self):
        self.rect = Rect(self.x, self.y, 32, 32)
        return pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def checkCollision(self, p):
        collide = pygame.Rect.colliderect(p, self.rect)
        if collide:
            self.x = random.randint(100, rW - 100)
            self.y = random.randint(100, rH - 100)
            self.count += 1

    def returnCount(self):
        return self.count
