import pygame
from pygame.locals import *

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (255, 0, 0)

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect)

    def move(self, direction, distance=32):
        if direction == "L":
            self.x -= distance
        elif direction == "R":
            self.x += distance
        elif direction == "U":
            self.y -= distance
        elif direction == "D":
            self.y += distance
        self.update_rect()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def update_rect(self):
        self.rect = (self.x, self.y)

    def get_rect(self):
        return self.rect

    def get_position(self):
        return self.x, self.y

    def getX(self):
        return self.x

    def getY(self):
        return self.y
