import pygame
from pygame.locals import *
from fruit import Fruits
from blocks import Block
import time

# game
pygame.init()
rW = 906
rH = 608
screen = pygame.display.set_mode((rW, rH))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game || Anahad")
white = (255, 255, 255)

# variables
x = 50
y = 50
playerRect = Rect(x, y, 32, 32)
running = True
speed = 0.2
fruit = Fruits(200, 200)
last_key = ""

# returns the rectangle
def drawPlayer(playerRect):
    return pygame.draw.rect(screen, (0, 0, 255), playerRect)

# checks for boundaries (if player moves out of the screen)
def checkBoundaries(x, y):
    if x <= 0 or x >= rW or y <= 0 or y >= rH:
        return False
        print("Game Over! You went out of bounds.")
    else:
        return True

blocks = [[0] * 4 for i in range(100)]

for i in range(0, 100):
    blocks[i] = Block(x, y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_LEFT]:
        last_key = "L"
    elif keysPressed[pygame.K_RIGHT]:
        last_key = "R"
    elif keysPressed[pygame.K_UP]:
        last_key = "U"
    elif keysPressed[pygame.K_DOWN]:
        last_key = "D"

    if last_key == "L":
        x -= speed + (fruit.returnCount() * 0.025)
    elif last_key == "R":
        x += speed + (fruit.returnCount() * 0.025)
    elif last_key == "U":
        y -= speed + (fruit.returnCount() * 0.025)
    elif last_key == "D":
        y += speed + (fruit.returnCount() * 0.025)

    screen.fill(white)

    playerRect = Rect(x, y, 32, 32)
    drawPlayer(playerRect)
    running = checkBoundaries(x, y)

    fruit.checkCollision(playerRect)
    fruit.drawFruit()

    for i in range(0, fruit.returnCount()):

        if i != 0:
            blocks[i].drawBlocks()
            blocks[i].adjustDirection(last_key, blocks[i-1].getX(), blocks[i-1].getY())
        else:
            blocks[0].drawBlocks()
            blocks[0].adjustDirection(last_key, x, y)

    font = pygame.font.Font("MoonbrightDemo-1GGn2.ttf", 32)
    text = font.render("SCORE: " + str(fruit.returnCount()), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (100, 100)

    screen.blit(text, textRect)

    pygame.display.flip()

pygame.quit()
