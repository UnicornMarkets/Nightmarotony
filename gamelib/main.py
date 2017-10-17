'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data
import pygame
from gamelib.character import Character
from gamelib.shelf import Shelf
from pygame.locals import *

class Game(object):

    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.grass = pygame.image.load("resources/images/grass.png")
        self.player = Character(self.sprites)
        self.shelf = Shelf((self.sprites))
        self.shelf_info = pygame.image.load("resources/images/shelf_info.png")

    def main(self):

        while True:
            self.views()
            self.event_processor()


    def views(self):
        self.screen.fill(0)
        for x in range(0, self.width // self.grass.get_width() + 1):
            for y in range(0, self.height // self.grass.get_height() + 1):
                self.screen.blit(self.grass, (x * 100, y * 100))

        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.shelf.image, self.shelf.rect)
        pygame.display.flip()

    def event_processor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                self.player.update(self)

            if self.player.rect.colliderect(
                    self.shelf.rect) and event.type == pygame.MOUSEBUTTONDOWN:
                screen1 = pygame.display.set_mode((self.width, self.height))
                close = 1
                while close:
                    screen1.fill(0)
                    screen1.blit(self.shelf_info, [40, 100])
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            close = 0