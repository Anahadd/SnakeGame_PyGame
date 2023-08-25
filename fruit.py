import pygame
from pygame.locals import *
import random

rW = 906
rH = 608

class Fruits:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 32, 32)
        self.count = 0

    def drawFruit(self, screen):
        self.rect.topleft = (self.x, self.y)
        return pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def checkCollision(self, p):
        collide = pygame.Rect.colliderect(p, self.rect)
        if collide:
            self.reposition()
            self.count += 1
            return True
        return False

    def reposition(self):
        self.x = random.randint(0, rW - 32)
        self.y = random.randint(0, rH - 32)

    def returnCount(self):
        return self.count

