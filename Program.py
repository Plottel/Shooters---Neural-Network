import pygame, sys
import pygame.time
import pygame.transform
from pygame.rect import Rect
from Renderer import Renderer
import Input
from Entity import Entity
import GameController
#import cProfile
import random
import Params
import Utils

clock = pygame.time.Clock()

pygame.init()
Input.init()
GameController.init()

if __name__ == "__main__":
    #cProfile.run('run()')
    while True:
        clock.tick(60)
        Input.process_events()
        Renderer.clear_screen()

        GameController.run()

        pygame.display.flip()
