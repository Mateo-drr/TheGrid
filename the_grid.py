import numpy as np
from identity_disk import IdentityDisk
from grid_viewer import GridViewer
import random

def field_of_view(program: IdentityDisk, grid):
    visible_field = {}
    for dy in range(-program.fov["y"], program.fov["y"]+1):
        for dx in range(-program.fov["x"], program.fov["x"]+1):
            check_x = program.position["x"] + dx
            check_y = program.position["y"] + dy
            if (check_y, check_x) in grid:
                visible_field[(check_y, check_x)] = grid[(check_y, check_x)]
    return visible_field

# init pygame
grid_viewer = GridViewer()

# Create infinite grid using dictionary (only stores occupied cells)
grid = {}

# Place some food and drinks in the world
grid[(15, 25)] = 2  # Food
grid[(35, 40)] = 3  # Drink
grid[(-10, 20)] = 2  # Food in negative space
grid[(50, -30)] = 3  # Drink in negative space

# Create the program
tron = IdentityDisk()

# Game loop
while grid_viewer.events["running"]:

    if random.random() < 0.1:
        # spawn random food
        grid[(random.randint(-100,100), random.randint(-100,100))] = 2

    grid_viewer.process_events()

    visible_field = field_of_view(tron, grid)
    tron.look(visible_field)
    ans, food_pos = tron.can_see_food()
    print("FOOD?", ans, food_pos)

    # Update program movement
    if ans is True:
        tron.move_toward(food_pos[0], food_pos[1])

        if tron.position["y"] == food_pos[0] and tron.position["x"] == food_pos[1]:
            del grid[food_pos]  # Eat the food!

    if tron.desire_move():
        tron.move()
        print(grid)

    grid_viewer.draw([tron], grid)

# Quit pygame
grid_viewer.quit()
