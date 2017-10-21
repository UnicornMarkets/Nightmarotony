import pygame
import random
try:
    from gamelib import data, const, state
except:
    import data
    import const
    import state
from math import sqrt

class Shelf(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Shelf, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                     "Game", "shelf.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def start_game(self, level):
        state.State(level, state_name='shelf').run_state()

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Door, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                      "Game", "door.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def start_game(self, level):
        level.result = state.State(level, state_name='door').run_state()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, *groups):
        super(Block, self).__init__(*groups)
        number = str(random.randint(1, 4))
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                         "maze tiles", color + "tiles-" + number + ".png")), (size, size))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
