
import numpy as np
import random

class IdentityDisk:
    def __init__(self):
        self.position = {"y":10, "x":10}
        self.fov = {"y":10, "x":10}

    def desire_move(self):
        # should i move?
        move_around = random.random() < 0.1
        return move_around

    # def desire_food(self):

    def can_see_food(self, visible_grid: dict):
        for key,value in visible_grid.items():
            if value == 2:
                return True
        return False


    def move(self):
        delta_x = np.random.randint(low=-1,high=1+1)
        delta_y = np.random.randint(low=-1,high=1+1)
        self.position["x"] += delta_x
        self.position["y"] += delta_y
