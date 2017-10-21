import pygame
try:
    from gamelib import data, const, state
except:
    import data
    import const
    import state
from math import sqrt

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Door, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                      "Game", "door.png")), (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self.rect = pygame.rect.Rect((const.BLOCK_SIZE, 6 * const.BLOCK_SIZE),
                                            self.image.get_size())

    def start_game(self, level):
        level.result = state.State(level, state_name='door').run_state()
