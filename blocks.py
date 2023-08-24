import pygame
from pygame.locals import *

rW = 906
rH = 608
screen = pygame.display.set_mode((rW, rH))
black = (0, 0, 0)

class blocks:
    def __init__(self, count, x, y):
        self.count = count
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 32, 32)

    def drawBlocks(self):
        return pygame.draw.rect(screen, black, self.rect)

    def updateBlockCoordinate(self, last_key):
        if last_key == "D":
            pass
        elif last_key == "U":
            pass
        elif last_key == "R":
            pass
        elif last_key == "L":
            pass
