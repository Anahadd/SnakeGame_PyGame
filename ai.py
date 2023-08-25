import pygame
from pygame.locals import *
from fruit import Fruits
from blocks import Block
import time
import numpy as np


# game
pygame.init()
rW = 800
rH = 800
screen = pygame.display.set_mode((rW, rH))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game By Anahad")
white = (255, 255, 255)

# variables
x = 192
y = 192
playerRect = Rect(x, y, 32, 32)
running = True
speed = 32
last_key = ""
fruit = Fruits(192, 288)
snake_blocks = [Block(x, y)]

# q learning parameters
updateCoordinates = ()
updateCoordinatesBlocks = [[0] * 1 for i in range(625)]
updateCoordinatesFruit = ()

grid_state = np.full((25, 25), "empty", dtype=object)


# draws player
def drawPlayer(block):
    pygame.draw.rect(screen, (0, 255, 0), block.get_rect())


def checkBoundaries(block, incX, incY):
    # boundary checking
    x, y = block.getX() + incX, block.getY() + incY
    if x < 0 or x > rW or y < 0 or y > rH:
        print("Game Over! You went out of bounds.")
        return False
    else:
        return True


def draw_grid():
    # draws the grid lines
    for x in range(0, rW, 32):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, rH))
    for y in range(0, rH, 32):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (rW, y))

def pixel_to_grid(x, y):
    return x // 32, y // 32

def updateGrid(updateCoordinates, updateCoordinatesBlocks, updateCoordinatesFruit):
    grid_state[:, :] = "empty"

    head_x, head_y = pixel_to_grid(*updateCoordinates)
    grid_state[head_x][head_y] = "head of snake"

    for b in updateCoordinatesBlocks:
        block_x, block_y = pixel_to_grid(*b)
        grid_state[block_x][block_y] = "snake"

    fruit_x, fruit_y = pixel_to_grid(*updateCoordinatesFruit)
    grid_state[fruit_x][fruit_y] = "food"

def would_collide(x, y, blocks):
    for block in blocks:
        if block.getX() == x and block.getY() == y:
            return True
    return False


'''def checkDir(x, y, dir):
    row = x // 32
    col = y // 32

    count = 0

    if dir == "L":
        for i in range(0, col):
            if grid_state[row][i] == "empty":
                count += 1

        if count == col:
            return "L"
        else:
            return "U"

    elif dir == "R":
        for i in range(col + 1, 25):
            if grid_state[row][i] == "empty":
                count += 1

        if count == 24 - col:
            return "R"
        else:
            return "U"

    elif dir == "U":
        for i in range(0, row):
            if grid_state[i][col] == "empty":
                count += 1
        if count == row:
            return "U"
        else:
            return "R"

    elif dir == "D":
        for i in range(row + 1, 25):
            if grid_state[i][col] == "empty":
                count += 1
        if count == 24 - row:
            return "D"
        else:
            return "R"
'''
def pathToFood(x_one, x_two, y_one, y_two, last_key):
    # manhattan distance
    total_x = x_two - x_one
    total_y = y_two - y_one

    dX = int(total_x / 32)
    dY = int(total_y / 32)

    if dX != 0:
        if dX > 0 or dX < rW:
            if dX > 0:
                last_key = "L"
                return "R"
            else:
                last_key = "R"
                return "L"
    elif dY != 0:
        if dY > 0 or dY < rH:
            if dY > 0:
                last_key = "U"
                return "D"
            else:
                last_key = "D"
                return "U"
    else:
        return 'S'


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # stores boolean list of keys pressed
    keysPressed = pygame.key.get_pressed()

    # get the last key pressed to replicate snake movement
    if keysPressed[pygame.K_LEFT] and last_key != "R":
        last_key = "L"
    elif keysPressed[pygame.K_RIGHT] and last_key != "L":
        last_key = "R"
    elif keysPressed[pygame.K_UP] and last_key != "D":
        last_key = "U"
    elif keysPressed[pygame.K_DOWN] and last_key != "U":
        last_key = "D"

    # set parameters for snake head (x, y)
    head_x, head_y = snake_blocks[0].getX(), snake_blocks[0].getY()

    d = pathToFood(head_x, fruit.getX(), head_y, fruit.getY(), last_key)

    if d == "L" and not would_collide(head_x - speed, head_y, snake_blocks[1:]) and checkBoundaries(snake_blocks[0],-32, 0):
        head_x -= speed
    elif d == "R" and not would_collide(head_x + speed, head_y, snake_blocks[1:]) and checkBoundaries(snake_blocks[0],32, 0):
        head_x += speed
    elif d == "U" and not would_collide(head_x, head_y - speed, snake_blocks[1:]) and checkBoundaries(snake_blocks[0],0, -32):
        head_y -= speed
    elif d == "D" and not would_collide(head_x, head_y + speed, snake_blocks[1:]) and checkBoundaries(snake_blocks[0],0, 32):
        head_y += speed

    # create new head
    new_head = Block(head_x, head_y)
    snake_blocks.insert(0, new_head)

    # check for collision w fruit
    if fruit.checkCollision(new_head.get_rect()):
        fruit.reposition()
    else:
        snake_blocks.pop()

    # bg
    screen.fill((0, 0, 255))

    # boundary check
    running = checkBoundaries(snake_blocks[0], 0, 0)

    # check if snake hit itself
    for i, block in enumerate(snake_blocks):
        drawPlayer(block)
        if i < 2:
            continue

        if block.get_rect().colliderect(snake_blocks[0].get_rect()):
            running = False
            print("Collision With Self")
            print(snake_blocks[1].getX(), snake_blocks[1].getY())
            break

    snake_head_coord = (snake_blocks[0].getX(), snake_blocks[0].getY())
    snake_body_coords = [(block.getX(), block.getY()) for block in snake_blocks[1:]]
    fruit_coord = (fruit.getX(), fruit.getY())
    updateGrid(snake_head_coord, snake_body_coords, fruit_coord)

    # draw gui
    fruit.drawFruit(screen)
    draw_grid()
    font = pygame.font.Font("MoonbrightDemo-1GGn2.ttf", 32)
    text = font.render("SCORE: " + str(len(snake_blocks) - 1), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (32, 32)
    screen.blit(text, textRect)

    pygame.display.flip()

    # fps
    clock.tick(50)

pygame.quit()
