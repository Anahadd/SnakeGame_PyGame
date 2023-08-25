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
speed = 10
fruit = Fruits(200, 200)
last_key = ""

snake_blocks = [Block(x, y)]

def drawPlayer(block):
    pygame.draw.rect(screen, (0, 255, 0), block.get_rect())


def checkBoundaries(block):
    x, y = block.getX(), block.getY()
    if x <= 0 or x >= rW or y <= 0 or y >= rH:
        print("Game Over! You went out of bounds.")
        return False
    else:
        return True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_LEFT] and last_key != "R":
        last_key = "L"
    elif keysPressed[pygame.K_RIGHT] and last_key != "L":
        last_key = "R"
    elif keysPressed[pygame.K_UP] and last_key != "D":
        last_key = "U"
    elif keysPressed[pygame.K_DOWN] and last_key != "U":
        last_key = "D"

    head_x, head_y = snake_blocks[0].getX(), snake_blocks[0].getY()

    if last_key == "L":
        head_x -= speed
    elif last_key == "R":
        head_x += speed
    elif last_key == "U":
        head_y -= speed
    elif last_key == "D":
        head_y += speed

    new_head = Block(head_x, head_y)
    snake_blocks.insert(0, new_head)

    if fruit.checkCollision(new_head.get_rect()):
        fruit.reposition()
    else:
        snake_blocks.pop()

    screen.fill(white)

    for block in snake_blocks:
        drawPlayer(block)

    running = checkBoundaries(snake_blocks[0])

    fruit.drawFruit(screen)

    font = pygame.font.Font("MoonbrightDemo-1GGn2.ttf", 32)
    text = font.render("SCORE: " + str(len(snake_blocks) - 1), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (100, 100)
    screen.blit(text, textRect)

    pygame.display.flip()
    clock.tick(15 + fruit.returnCount())

pygame.quit()
