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
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
queue = []
visited = []

# q learning parameters
updateCoordinates = ()
updateCoordinatesBlocks = [[0] * 1 for i in range(625)]
updateCoordinatesFruit = ()

grid_state = np.full((25, 25), "empty", dtype=object)

new_head_x = 192
new_head_y = 192

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

def bfs_maze_solver(start, end_node, maze_array):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    queue = [(start, [])]  # Each item has a node and a path to that node
    visited = set()

    while queue:
        current_node, current_path = queue.pop(0)

        if current_node == end_node:
            return current_path + [end_node]

        for dir in directions:
            neighbor_node = (current_node[0] + dir[0], current_node[1] + dir[1])
            if (0 <= neighbor_node[0] < len(maze_array)) and (0 <= neighbor_node[1] < len(maze_array[0])):  # In bounds
                if neighbor_node not in visited and maze_array[neighbor_node[0]][neighbor_node[1]] not in ["snake", "head of snake"]:
                    visited.add(neighbor_node)
                    queue.append((neighbor_node, current_path + [current_node]))

    return None

def updateCoordinate(x, r, c):
    return (x[0] + r, x[1] + c)

def updateGrid(updateCoordinates, updateCoordinatesBlocks, updateCoordinatesFruit):
    grid_state[:, :] = "empty"

    head_x, head_y = pixel_to_grid(*updateCoordinates)
    grid_state[head_x][head_y] = "head of snake"

    for b in updateCoordinatesBlocks:
        block_x, block_y = pixel_to_grid(*b)
        grid_state[block_x][block_y] = "snake"

    fruit_x, fruit_y = pixel_to_grid(*updateCoordinatesFruit)
    grid_state[fruit_x][fruit_y] = "food"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    head_x, head_y = snake_blocks[0].getX(), snake_blocks[0].getY()
    snake_head_coord = pixel_to_grid(head_x, head_y)
    fruit_coord = pixel_to_grid(fruit.getX(), fruit.getY())

    bfs_path = bfs_maze_solver(snake_head_coord, fruit_coord, grid_state)

    if bfs_path and len(bfs_path) > 1:
        next_step = bfs_path[1]
        x_move, y_move = (next_step[0] - snake_head_coord[0]) * 32, (next_step[1] - snake_head_coord[1]) * 32
        new_head_x, new_head_y = head_x + x_move, head_y + y_move

        new_head = Block(new_head_x, new_head_y)
        snake_blocks.insert(0, new_head)

        if fruit.checkCollision(new_head.get_rect()):
            fruit.reposition(snake_blocks)
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

    snake_body_coords = [(block.getX(), block.getY()) for block in snake_blocks[1:]]
    updateGrid(snake_head_coord, snake_body_coords, fruit_coord)

    # draw gui
    fruit.drawFruit(screen)
    draw_grid()
    font = pygame.font.Font("MoonbrightDemo-1GGn2.ttf", 32)
    text = font.render("SCORE: " + str(len(snake_blocks) - 1), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (64, 64)
    screen.blit(text, textRect)

    pygame.display.flip()

    if len(snake_blocks) == 625:
        running = False
        print("snake wins")

    # fps
    clock.tick(50)

pygame.quit()


