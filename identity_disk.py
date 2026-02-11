
import numpy as np
import random

class IdentityDisk:
    def __init__(self):
        self.position = {"y":10, "x":10}
        self.fov = {"y":10, "x":10}
        self.visible_grid = None

    def desire_move(self):
        # should i move?
        move_around = random.random() < 0.1
        return move_around

    # def desire_food(self):

    def look(self, visible_grid: dict):
        self.visible_grid = visible_grid

    def can_see_food(self):
        for key,value in self.visible_grid.items():
            if value == 2:
                return True, key
        return False, None

    def move_toward(self, target_y, target_x):
        # Calculate direction to target
        dy = target_y - self.position["y"]
        dx = target_x - self.position["x"]

        # Move one step in that direction
        # np.sign() returns -1, 0, or 1
        move_y = np.sign(dy)
        move_x = np.sign(dx)

        self.position["y"] += move_y
        self.position["x"] += move_x

    def land_or_water(self, target_y, target_x):

        if len(self.visible_grid) == 0:
            return None

        if self.visible_grid[(target_y, target_x)] == 0:
            return "land"
        elif self.visible_grid[(target_y, target_x)] == 1:
            return "water"
        else:
            return None


    def move(self):
        delta_x = np.random.randint(low=-1,high=1+1)
        delta_y = np.random.randint(low=-1,high=1+1)

        new_x, new_y =  self.position["x"] + delta_x, self.position["y"] + delta_y
        match self.land_or_water(new_y, new_x):
            case "land":
                self.position["x"] = new_x
                self.position["y"] = new_y
            case "water":
                pass # remain in the same position
