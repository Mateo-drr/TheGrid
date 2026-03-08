
from noise import pnoise2

MAP_LEGEND = {
    "land": 0,
    "water": 1,
    "food": 2,
    "drink": 3
}

class Grid:
    def __init__(self):
        self.terrain = {
            "scale": 0.005,
            "water_th": 0.0,
        }

        self.objects = {} # same grid ([y,x]) logic

    def terrain_generator(self, x: int, y: int) -> str:
        # More octaves = more detail layers
        # Persistence controls how much each octave contributes
        height = pnoise2(x * self.terrain["scale"], y * self.terrain["scale"],
                         octaves=4,  # More layers
                         persistence=0.5,  # Each octave is 50% of previous
                         lacunarity=2.0)  # Frequency multiplier
        # height [-1;1]
        if height < self.terrain["water_th"]:
            return "water"
        else:
            return "land"

    def place_object(self, x: int, y: int, object_type: str):
        self.objects[(y,x)] = object_type

    def remove_object(self, x: int, y: int):
        if (y, x) in self.objects:
            del self.objects[(y,x)]
        else:
            raise KeyError("Tried to remove object from grid that doesn't exist", x,y)