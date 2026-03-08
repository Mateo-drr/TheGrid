
import numpy as np
import random

class IdentityDisk:
    def __init__(self, heritage=None):

        # genes to add:
        #
        # skills:
        # tanks, cars, destroyers
        suit_colors = ("blue", "white", "green", "red", "orange")

        if heritage is None:
            self.genes = {
                "suit": random.choice(suit_colors),
                "agility": random.randint(0, 9),
                "aggressiveness": random.randint(0, 9),
                "stamina": random.randint(0, 9),
                "charisma": random.randint(0, 9),
                "strength": random.randint(0, 9),
            }
        else:
            self.genes = heritage

        self.mutation_rate = 0.05 # environment should be able to affect this

        self.mutate()

        # TODO add skills dictionary

    def crossover(self, other):
        """Uniform crossover with another IdentityDisk. Returns two children."""
        # TODO add a way of weighing parent importance i.e. gene dominance
        offspring = {}
        for key in self.genes.keys():
            if random.random() < 0.5:
                offspring[key] = self.genes[key]
            else:
                offspring[key] = other.genes[key]

        return IdentityDisk(heritage=offspring)

    def mutate(self):
        """Randomly mutate each gene with a given probability."""
        for key in self.genes.keys():
            if key != "suit":
                if random.random() < self.mutation_rate:
                    self.genes[key] = random.randint(0,9)

class Program:
    def __init__(self, identity_disk: IdentityDisk):

        self.identity_disk = identity_disk

        self.position = {"y": 10, "x": 10}
        self.fov = {"y": 10, "x": 10}
        self.visible_grid = None
        self.visible_objects = None


    def desire_move(self):
        # should i move?
        move_around = random.random() < 0.1
        return move_around

    def look(self, visible_grid: dict, visible_objects: dict):
        self.visible_grid = visible_grid
        self.visible_objects = visible_objects


    def can_see_food(self):
        for key, value in self.visible_objects.items():
            if value == "food" and self.visible_grid[key] != "water":
                return True, key
        return False, None


    def move_toward(self, target_y, target_x):
        # WATER CHECK HAS TO BE DONE BEFORE CALLING THIS
        # Calculate direction to target
        dy = target_y - self.position["y"]
        dx = target_x - self.position["x"]

        # Move one step in that direction
        # np.sign() returns -1, 0, or 1
        move_y = np.sign(dy)
        move_x = np.sign(dx)

        self.position["y"] += move_y
        self.position["x"] += move_x

    def move(self):
        delta_x = np.random.randint(low=-1,high=1+1)
        delta_y = np.random.randint(low=-1,high=1+1)

        new_x, new_y =  self.position["x"] + delta_x, self.position["y"] + delta_y
        match self.visible_grid[(new_y, new_x)]:
            case "land":
                self.position["x"] = new_x
                self.position["y"] = new_y
            case "water":
                pass # remain in the same position