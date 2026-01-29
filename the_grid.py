import pygame
import numpy as np
from identity_disk import IdentityDisk

def field_of_view(program: IdentityDisk, grid):
    visible_field = {}
    for dy in range(-program.fov["y"], program.fov["y"]+1):
        for dx in range(-program.fov["x"], program.fov["x"]+1):
            check_x = program.position["x"] + dx
            check_y = program.position["y"] + dy
            if (check_y, check_x) in grid:
                visible_field[(check_y, check_x)] = grid[(check_y, check_x)]
    return visible_field

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 10  # Each grid cell will be 10x10 pixels

# Viewport dimensions (how many cells visible on screen)
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Create the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Grid")

# Create clock for controlling frame rate
clock = pygame.time.Clock()

# Create infinite grid using dictionary (only stores occupied cells)
grid = {}

# Place some food and drinks in the world
grid[(15, 25)] = 2  # Food
grid[(35, 40)] = 3  # Drink
grid[(-10, 20)] = 2  # Food in negative space
grid[(50, -30)] = 3  # Drink in negative space

# Colors (RGB)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)

# Create the program
tron = IdentityDisk()

# Game loop
running = True
clicking = False
click_x, click_y = None, None
camera_x, camera_y = 0, 0

while running:
    # Handle events
    for event in pygame.event.get():

        match event.type:

            case pygame.QUIT:
                running = False

            case pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                clicking = True

            case pygame.MOUSEBUTTONUP:
                clicking = False
                click_x, click_y = None, None

            case pygame.MOUSEMOTION:
                # Only process movement if button is held
                if clicking and click_x is not None and click_y is not None:
                    mouse_x, mouse_y = event.pos
                    camera_x = mouse_x - click_x
                    camera_y = mouse_y - click_y


    visible_field = field_of_view(tron, grid)
    print("FOOD?", tron.can_see_food(visible_field))

    # Update program movement
    if tron.desire_move():
        tron.move()
        print(grid)

    # Fill screen with black
    screen.fill(BLACK)

    # Calculate visible range
    visible_y_start = camera_y - (GRID_HEIGHT // 2)
    visible_y_end = camera_y + (GRID_HEIGHT // 2)
    visible_x_start = camera_x - (GRID_WIDTH // 2)
    visible_x_end = camera_x + (GRID_WIDTH // 2)

    # Draw only visible cells
    for y in range(visible_y_start, visible_y_end):
        for x in range(visible_x_start, visible_x_end):
            # Calculate screen position
            screen_x = (x - visible_x_start) * CELL_SIZE
            screen_y = (y - visible_y_start) * CELL_SIZE

            # Draw the program
            if tron.position["y"] == y and tron.position["x"] == x:
                pygame.draw.rect(screen, CYAN, (screen_x, screen_y, CELL_SIZE*2, CELL_SIZE*2))
            # Draw food and drinks from the grid dictionary
            elif (y, x) in grid:
                if grid[(y, x)] == 2:  # Food
                    pygame.draw.rect(screen, YELLOW, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                elif grid[(y, x)] == 3:  # Drink
                    pygame.draw.rect(screen, BLUE, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

    # Update display
    pygame.display.flip()

    # Control frame rate (60 FPS)
    clock.tick(60)

# Quit pygame
pygame.quit()