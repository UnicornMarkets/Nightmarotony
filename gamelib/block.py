import pygame
try:
    from gamelib import data
except:
    import data

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, *groups):
        super(Block, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
            "Game", "block.png")), (size, size))
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
