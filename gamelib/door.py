import pygame
try:
    from gamelib import data
except:
    import data
from math import sqrt

class Door(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Door, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath("Game", "door.png")), (100,200))
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((300, 0), (image_size[0], image_size[1]))
