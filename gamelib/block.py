import pygame
import random
try:
    from gamelib import data
except:
    import data

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, *groups):
        super(Block, self).__init__(*groups)
        number = str(random.randint(1, 4))
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                         "maze tiles", color + "tiles-" + number + ".png")), (size, size))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
