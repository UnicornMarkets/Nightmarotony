import pygame
try:
    import data
except:
    from gamelib import data
from math import sqrt

class Shelf(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Shelf, self).__init__(*groups)
        self.image = pygame.image.load(data.filepath("Game", "shelf.png"))
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((0, 30), (image_size[0] / 2, image_size[1] / 2))
