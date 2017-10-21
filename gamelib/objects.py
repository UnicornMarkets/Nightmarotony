import pygame
import random
try:
    from gamelib import data, const, state
except:
    import data
    import const
    import state
from math import sqrt

class VRgoggles(pygame.sprite.Sprite):
    def __init__(self, x, y, pin_code, *groups):
        super(VRgoggles, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                     "Game", "vrgoggles.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.message = str(random.randint(1,10))
        self.pin_code = None

    def start_game(self, level):
        level.transition(self.message)

class Computer(pygame.sprite.Sprite):
    def __init__(self, x, y, pin_code, *groups):
        super(Computer, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                     "Game", "computer.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.pin_code = pin_code

    def start_game(self, level):
        state.State(level, 'computer', self).run_state()

class Shelf(pygame.sprite.Sprite):
    def __init__(self, x, y, pin_code, *groups):
        super(Shelf, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                     "Game", "shelf.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.pin_code = pin_code

    def start_game(self, level):
        state.State(level, 'shelf', self).run_state()

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, pin_code, *groups):
        super(Door, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                      "Game", "door.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.tries = 0
        self.pin_code = pin_code

    def start_game(self, level):
        result = state.State(level, 'door', self).run_state()
        if result == -1:
            self.tries += 1
        elif result > 0:
            level.result = result

        if self.tries == 3:
            level.result = -200

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, *groups):
        super(Block, self).__init__(*groups)
        number = str(random.randint(1, 4))
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                         "maze tiles", color + "tiles-" + number + ".png")), (size, size))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
