import pygame
try:
    from gamelib import data
except:
    import data

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, *groups):
        super(Block, self).__init__(*groups)
        self.x = x
        self.y = y
        self.block = pygame.transform.scale(pygame.image.load(data.filepath(
            "Game", "block.png")), (size, size))

    def create_wall(self, sprites):
        wall.image = self.block
        wall.rect = pygame.rect.Rect((self.x, self.y), self.block.get_size())
        sprites.add(self.walls)

    def update(self):
        pass
