
import numpy as np
from identity_disk import Program, IdentityDisk
from grid_viewer import GridViewer
from the_grid import Grid
import random

def field_of_view(program: Program, grid):
    visible_terrain = {}
    visible_objects = {}
    for dy in range(-program.fov["y"], program.fov["y"]+1):
        for dx in range(-program.fov["x"], program.fov["x"]+1):
            check_x = program.position["x"] + dx
            check_y = program.position["y"] + dy

            # first check visible objects
            if (check_y, check_x) in grid.objects:
                visible_objects[(check_y, check_x)] = grid.objects[(check_y, check_x)]

            # check if terrain is land or water
            visible_terrain[(check_y, check_x)] = grid.terrain_generator(check_x, check_y)

    return visible_terrain, visible_objects

# init pygame
grid_viewer = GridViewer()

# Create infinite grid using dictionary (only stores occupied cells)
# grid = {}

# Place some food and drinks in the world
# grid[(15, 25)] = 2  # Food
# grid[(35, 40)] = 3  # Drink
# grid[(-10, 20)] = 2  # Food in negative space
# grid[(50, -30)] = 3  # Drink in negative space

grid = Grid()

# Create the program
tron = Program(IdentityDisk())

# Game loop
while grid_viewer.events["running"]:

    if random.random() < 0.1:
        # spawn random food
        grid.place_object(random.randint(-100,100), random.randint(-100,100), "food")

    grid_viewer.process_events()

    visible_terrain, visible_objects = field_of_view(tron, grid)
    tron.look(visible_terrain, visible_objects)
    ans, food_pos = tron.can_see_food()
    print("FOOD?", ans, food_pos, visible_objects)

    # Update program movement
    if ans is True:
        tron.move_toward(food_pos[0], food_pos[1])

        if tron.position["y"] == food_pos[0] and tron.position["x"] == food_pos[1]:
            grid.remove_object(y = food_pos[0], x = food_pos[1])  # Eat the food!

    if tron.desire_move():
        tron.move()
        print(grid.objects)

    grid_viewer.draw([tron], grid)

# Quit pygame
grid_viewer.quit()
