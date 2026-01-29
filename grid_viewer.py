import pygame


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
            "blue": (0, 100, 255)
        }


