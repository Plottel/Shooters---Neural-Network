import pygame

class Renderer:
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

    # This is the surface used as the first argument for most drawing methods
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    TILE_SIZE = 24
    COLOR_BLACK = 0, 0, 0
    COLOR_WHITE = 255, 255, 255
    COLOR_BLUE = 0, 0, 255
    COLOR_GREEN = 0, 255, 0
    COLOR_RED = 255, 0, 0

    @staticmethod
    def clear_screen():
        Renderer.SCREEN.fill((128, 128, 128))
