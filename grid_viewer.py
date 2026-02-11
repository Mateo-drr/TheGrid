import pygame
from identity_disk import IdentityDisk
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
            "light_blue": (110, 130, 150)
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
            "land": {
                "color": self.colors["black"],
                "value": 0,
            },
            "water": {
                "color": self.colors["light_blue"],
                "value": 1,
            }
            # TODO add food
        }

        self.camera_pos = {"x":0, "y":0}

    def process_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.events["running"] = False
                case pygame.MOUSEBUTTONDOWN:
                    self.events["click"]["x"], self.events["click"]["y"] = event.pos
                    self.events["clicking"] = True
                case pygame.MOUSEBUTTONUP:
                    self.events["clicking"] = False
                    self.events["click"]["x"], self.events["click"]["y"] = None, None
                case pygame.MOUSEMOTION:
                    # Only process movement if button is held
                    if self.events["clicking"] and self.events["click"]["x"] is not None and self.events["click"]["y"] is not None:
                        mouse_x, mouse_y = event.pos
                        self.camera_pos["x"] = mouse_x - self.events["click"]["x"]
                        self.camera_pos["y"] = mouse_y - self.events["click"]["y"]

    def get_visible_coords(self):
        # Calculate visible range
        visible_y_start = self.camera_pos["y"] - (self.grid_size["height"] // 2)
        visible_y_end = self.camera_pos["y"] + (self.grid_size["height"] // 2)
        visible_x_start = self.camera_pos["x"] - (self.grid_size["width"] // 2)
        visible_x_end = self.camera_pos["x"] + (self.grid_size["width"] // 2)
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

    def terrain_generator(self, x, y, scale: float = 0.1, water_th: float = 0.1):
        # Generate noise value (-1 to 1)
        height = pnoise2(x * scale, y * scale, octaves=2)
        if height < water_th:
            return self.cell2color["water"]
        else:
            return self.cell2color["land"]

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
                cell_info = self.terrain_generator(x, y, scale=0.01, water_th=0.01)

                pygame.draw.rect(
                    self.screen,
                    cell_info["color"],
                    (screen_x, screen_y, self.cell_size, self.cell_size)
                )
                grid[(y,x)] = cell_info["value"] # store terrain into grid dict

                # Draw food and drinks from the grid dictionary
                if (y, x) in grid:
                    if grid[(y, x)] == 2:  # Food
                        pygame.draw.rect(
                            self.screen,
                            self.colors["yellow"],
                            (screen_x, screen_y, self.cell_size, self.cell_size)
                        )
                    elif grid[(y, x)] == 3:  # Drink
                        pygame.draw.rect(
                            self.screen,
                            self.colors["blue"],
                            (screen_x, screen_y, self.cell_size, self.cell_size))

                # Draw the objects
                for generic_obj in objects:
                    if isinstance(generic_obj, IdentityDisk) and generic_obj.position["y"] == y and \
                            generic_obj.position["x"] == x:
                        pygame.draw.rect(
                            self.screen,
                            self.colors["cyan"],
                            (screen_x, screen_y, self.cell_size * 2, self.cell_size * 2)
                        )

        # Update display
        pygame.display.flip()

        # Control frame rate (60 FPS)
        self.clock.tick(60)

    def quit(self):
        pygame.quit()