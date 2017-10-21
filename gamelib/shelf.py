import pygame
try:
    from gamelib import data, const
except:
    import data
    import const
from math import sqrt

class Shelf(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Shelf, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                     "Game", "shelf.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((const.BLOCK_SIZE, 6 * const.BLOCK_SIZE),
                                                         self.image.get_size())
