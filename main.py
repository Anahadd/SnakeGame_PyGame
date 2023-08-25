import pygame
from pygame.locals import *
from fruit import Fruits
from blocks import Block

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
fruit = Fruits(320, 320)
snake_blocks = [Block(x, y)]

# q learning parameters
updateCoordinates = ()
updateCoordinatesBlocks = [[0] * 1 for i in range(625)]
updateCoordinatesFruit = ()
grid = []
grid_state = []

# for future use - q learning
for i in range(26):
    for k in range(26):
        grid.append((32 * i, 32 * k))
        grid_state.append("empty")

# draws player
def drawPlayer(block):
    pygame.draw.rect(screen, (0, 255, 0), block.get_rect())

def checkBoundaries(block):
    # boundary checking
    x, y = block.getX(), block.getY()
    if x <= 0 or x >= rW or y <= 0 or y >= rH:
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

# updates grid state
def updateGrid(updateCoordinates, updateCoordinatesBlocks, updateCoordinatesFruit):
    for i in range(0, len(grid)):
        current = grid[i]
        grid_state[i] = "empty"
        if current == updateCoordinates:
            grid_state[i] = "head of snake"
        for k in updateCoordinatesBlocks:
            if current == k:
                grid_state[i] = "snake"
        if current == updateCoordinatesFruit:
            grid_state[i] = "food"

    '''
    # prints out grid state (will not be needed)
    for row in range(25):
        for col in range(25):
            print(f"{grid_state[row * 25 + col]:4}", end=" ")
        print()

    print("\n\n\n")
    '''

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

    # directions
    if last_key == "L":
        head_x -= speed
    elif last_key == "R":
        head_x += speed
    elif last_key == "U":
        head_y -= speed
    elif last_key == "D":
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

    # update pos
    updateCoordinates = (x, y)
    for block in snake_blocks:
        drawPlayer(block)
        updateCoordinatesBlocks.append((block.getX(), block.getY()))
        
        # check if snake hit itself 
        if block != snake_blocks[0]:
            collide = pygame.Rect.colliderect(block.get_rect(), snake_blocks[0])
            if collide:
                running = False 
                print("Collision With Self")

    updateCoordinatesFruit = (fruit.getX(), fruit.getY())

    # setting grid parameters
    updateGrid(updateCoordinates, updateCoordinatesBlocks, updateCoordinatesFruit)

    # boundary check
    running = checkBoundaries(snake_blocks[0])

    # draw gui
    fruit.drawFruit(screen)
    draw_grid()
    font = pygame.font.Font("MoonbrightDemo-1GGn2.ttf", 16)
    text = font.render("SCORE: " + str(len(snake_blocks) - 1), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (32, 32)
    screen.blit(text, textRect)

    pygame.display.flip()

    # fps
    clock.tick(12)

pygame.quit()

