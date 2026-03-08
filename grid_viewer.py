import pygame
from identity_disk import Program
from noise import pnoise2

class GridViewer:
    def __init__(self):
        self.screen_size = {"width":800, "height":600}
        self.cell_size = 10
        self.grid_size = {
            "width": self.screen_size["width"] // self.cell_size,
            "height": self.screen_size["height"] // self.cell_size,
        }

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_size["width"], self.screen_size["height"])
        )
        pygame.display.set_caption("The Grid")
        self.clock = pygame.time.Clock()

        self.colors = {
            "black": (0, 0, 0),
            "cyan": (0, 255, 255),
            "yellow": (255, 255, 0),
            "blue": (0, 100, 255),
            "light_blue": (110, 130, 150),

            # "blue": (0, 100, 255),
            "white": (255, 255, 255),
            "green": (0, 255, 0),
            "red": (255, 0, 0),
            "orange": (255, 165, 0)
        }

        self.events = {
            "running": True,
            "clicking": False,
            "click": {
                "x": None,
                "y": None,
            },
        }

        self.cell2color = {
            "land": self.colors["black"],
            "water": self.colors["light_blue"],
            "food": self.colors["yellow"],
            "drink": self.colors["blue"],
            "program": self.colors["cyan"]
        }

        self.camera_pos = {"x":0, "y":0}
        self.camera_pos_on_click = {"x":0, "y":0}

        self.terrain = {
            "scale": 0.005,
            "water_th":0.0,
        }

    def process_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.events["running"] = False

                case pygame.MOUSEBUTTONDOWN:
                    self.events["click"]["x"], self.events["click"]["y"] = event.pos
                    self.events["clicking"] = True
                    self.camera_pos_on_click = {"x": self.camera_pos["x"], "y": self.camera_pos["y"]}

                case pygame.MOUSEBUTTONUP:
                    self.events["clicking"] = False
                    self.events["click"]["x"], self.events["click"]["y"] = None, None

                case pygame.MOUSEMOTION:
                    # Only process movement if button is held
                    if self.events["clicking"] and self.events["click"]["x"] is not None and self.events["click"]["y"] is not None:
                        mouse_x, mouse_y = event.pos
                        self.camera_pos["x"] = self.camera_pos_on_click["x"] + mouse_x - self.events["click"]["x"]
                        self.camera_pos["y"] = self.camera_pos_on_click["y"] + mouse_y - self.events["click"]["y"]

                case pygame.MOUSEWHEEL:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    zoom_factor = 1.1 if event.y > 0 else 0.9
                    new_cell_size = max(4, min(40, round(self.cell_size * zoom_factor)))

                    if new_cell_size != self.cell_size:
                        # World coordinate under the mouse before zoom
                        world_x = (
                            self.camera_pos["x"] +
                            mouse_x / self.cell_size +
                            self.grid_size["width"] // 2 -
                            self.screen_size["width"] // self.cell_size // 2
                        )
                        world_y = (
                            self.camera_pos["y"] +
                            mouse_y / self.cell_size +
                            self.grid_size["height"] // 2 -
                            self.screen_size["height"] // self.cell_size // 2
                        )

                        self.cell_size = new_cell_size

                        # Recalculate grid_size since cell_size changed
                        self.grid_size["width"] = self.screen_size["width"] // self.cell_size
                        self.grid_size["height"] = self.screen_size["height"] // self.cell_size

                        # Reposition camera so the same world point stays under mouse
                        self.camera_pos["x"] = (
                            world_x -
                            mouse_x / self.cell_size -
                            (
                                self.grid_size["width"] // 2 -
                                self.screen_size["width"] // self.cell_size // 2
                            )
                        )
                        self.camera_pos["y"] = (
                            world_y -
                            mouse_y / self.cell_size -
                            (
                                self.grid_size["height"] // 2 -
                                self.screen_size["height"] // self.cell_size // 2
                            )
                        )

    def get_visible_coords(self):
        # Calculate visible range
        visible_y_start = int(self.camera_pos["y"] - (self.grid_size["height"] // 2))
        visible_y_end = int(self.camera_pos["y"] + (self.grid_size["height"] // 2))
        visible_x_start = int(self.camera_pos["x"] - (self.grid_size["width"] // 2))
        visible_x_end = int(self.camera_pos["x"] + (self.grid_size["width"] // 2))
        return {
            "y": {
                "start": visible_y_start,
                "end": visible_y_end,
            },
            "x": {
                "start": visible_x_start,
                "end": visible_x_end,
            }

        }

    # def terrain_generator(self, x, y):
    #     # More octaves = more detail layers
    #     # Persistence controls how much each octave contributes
    #     height = pnoise2(x * self.terrain["scale"], y * self.terrain["scale"],
    #                      octaves=4,  # More layers
    #                      persistence=0.5,  # Each octave is 50% of previous
    #                      lacunarity=2.0)  # Frequency multiplier
    #     # height [-1;1]
    #     if height < self.terrain["water_th"]:
    #         return self.cell2color["water"]
    #     else:
    #         return self.cell2color["land"]

    def draw(self, objects, grid):

        self.screen.fill(self.colors["black"])

        view_xy = self.get_visible_coords()

        # Draw only visible cells
        for y in range(view_xy["y"]["start"], view_xy["y"]["end"]):
            for x in range(view_xy["x"]["start"], view_xy["x"]["end"]):
                # Calculate screen position
                screen_x = (x - view_xy["x"]["start"]) * self.cell_size
                screen_y = (y - view_xy["y"]["start"]) * self.cell_size

                # Create the terrain
                cell_info = grid.terrain_generator(x, y)
                pygame.draw.rect(
                    self.screen,
                    self.cell2color[cell_info],
                    (screen_x, screen_y, self.cell_size, self.cell_size)
                )
                # grid[(y,x)] = cell_info["value"] # store terrain into grid dict

                # Draw food and drinks from the grid dictionary
                if (y, x) in grid.objects:
                    if grid.objects[(y, x)] == "food":  # Food
                        pygame.draw.rect(
                            self.screen,
                            self.cell2color["food"],
                            (screen_x, screen_y, self.cell_size, self.cell_size)
                        )
                    elif grid.objects[(y, x)] == "drink":  # Drink
                        pygame.draw.rect(
                            self.screen,
                            self.cell2color["drink"],
                            (screen_x, screen_y, self.cell_size, self.cell_size))

                # Draw the objects
                for generic_obj in objects:
                    if (isinstance(generic_obj, Program) and
                        generic_obj.position["y"] == y and
                        generic_obj.position["x"] == x):
                        pygame.draw.rect(
                            self.screen,
                            # self.cell2color["program"],
                            self.colors[generic_obj.identity_disk.genes["suit"]],
                            (screen_x, screen_y, self.cell_size * 2, self.cell_size * 2)
                        )

        # Update display
        pygame.display.flip()

        # Control frame rate (60 FPS)
        self.clock.tick(60)

    def quit(self):
        pygame.quit()