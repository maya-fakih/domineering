import pygame

class DominosUI:
    def __init__(self):
        pass

    def draw_domino_V(self, win, x, y, tile_w, tile_h, color):
        # Main domino rectangle (same as before)
        pygame.draw.rect(win, color, (x, y, tile_w, tile_h * 2))

        # LIGHT EDGES (top + left)
        light = (
            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255)
        )

        # DARK EDGES (bottom + right)
        dark = (
            max(color[0] - 40, 0),
            max(color[1] - 40, 0),
            max(color[2] - 40, 0)
        )

        # Left inner edge
        pygame.draw.line(win, light, (x + 2, y + 2), (x + 2, y + 2 + tile_h * 2 - 4), 3)
        # Top inner edge
        pygame.draw.line(win, light, (x + 2, y + 2), (x + tile_w - 4, y + 2), 3)

        # Right inner edge
        pygame.draw.line(win, dark, (x + tile_w - 3, y + 2), (x + tile_w - 3, y + tile_h * 2 - 2), 3)
        # Bottom inner edge
        pygame.draw.line(win, dark, (x + 2, y + tile_h * 2 - 3), (x + tile_w - 3, y + tile_h * 2 - 3), 3)

    def draw_domino_H(self, win, x, y, tile_w, tile_h, color):
        # Main domino rectangle (same as before)
        pygame.draw.rect(win, color, (x, y, tile_w * 2, tile_h))

        # LIGHT EDGES (top + left)
        light = (
            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255)
        )

        # DARK EDGES (bottom + right)
        dark = (
            max(color[0] - 40, 0),
            max(color[1] - 40, 0),
            max(color[2] - 40, 0)
        )

        # Left inner edge
        pygame.draw.line(win, light, (x + 2, y + 2), (x + 2, y + tile_h - 4), 3)
        # Top inner edge
        pygame.draw.line(win, light, (x + 2, y + 2), (x + tile_w * 2 - 4, y + 2), 3)

        # Right inner edge
        pygame.draw.line(win, dark, (x + tile_w * 2 - 3, y + 2), (x + tile_w * 2 - 3, y + tile_h - 2), 3)
        # Bottom inner edge
        pygame.draw.line(win, dark, (x + 2, y + tile_h - 3), (x + tile_w * 2 - 3, y + tile_h - 3), 3)

