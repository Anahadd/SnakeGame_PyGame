import pygame
from pygame.locals import *
from fruit import Fruits

pygame.init()
rW = 906
rH = 608
screen = pygame.display.set_mode((rW, rH))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game || Anahad")
white = (255, 255, 255)

x = 50
y = 50
playerRect = Rect(x, y, 32, 32)
running = True

def drawPlayer(playerRect):
    return pygame.draw.rect(screen, (0, 0, 255), playerRect)

def checkBoundaries(x, y):
    if x <= 0 or x >= rW or y <= 0 or y >= rH:
        return False
        print("Game Over! You went out of bounds.")
    else:
        return True

speed = 0.2

fruit = Fruits(200, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_LEFT]:
        x -= speed + (fruit.returnCount() * 0.05)
    elif keysPressed[pygame.K_RIGHT]:
        x += speed + (fruit.returnCount() * 0.05)
    elif keysPressed[pygame.K_UP]:
        y -= speed + (fruit.returnCount() * 0.05)
    elif keysPressed[pygame.K_DOWN]:
        y += speed + (fruit.returnCount() * 0.05)

    screen.fill(white)

    playerRect = Rect(x, y, 32, 32)
    drawPlayer(playerRect)
    running = checkBoundaries(x, y)

    fruit.checkCollision(playerRect)
    fruit.drawFruit()

    pygame.display.flip()

pygame.quit()
