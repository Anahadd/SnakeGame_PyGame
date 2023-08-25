import pygame
from pygame.locals import *

rW = 906
rH = 608
screen = pygame.display.set_mode((rW, rH))
black = (0, 0, 0)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def drawBlocks(self):
        return pygame.draw.rect(screen, black, Rect(self.x, self.y, 32, 32))

    def adjustDirection(self, last_key, xPos, yPos):
        if last_key == "L":
            self.x = xPos + 32
            self.y = yPos
        elif last_key == "R":
            self.x = xPos - 32
            self.y = yPos
        elif last_key == "D":
            self.y = yPos - 32
            self.x = xPos
        elif last_key == "U":
            self.y = yPos + 32
            self.x = xPos

    def getX(self):
        return self.x

    def getY(self):
        return self.y
