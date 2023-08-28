import pygame
from pygame.locals import *
import random

rW = 800
rH = 800

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
            self.count += 1
            return True
        return False

    def reposition(self, x, y):
        while True:
            snake_x = x
            snake_y = y
            randomXPos = random.randint(0, rW - 32)
            randomYPos = random.randint(0, rH - 32)
            if (randomXPos % 32 == 0 and randomXPos != snake_x and randomYPos % 32 == 0 and randomYPos != snake_y):
                self.x = randomXPos
                self.y = randomYPos
                return False

    def returnCount(self):
        return self.count

    def getX(self):
        return self.x

    def getY(self):
        return self.y

