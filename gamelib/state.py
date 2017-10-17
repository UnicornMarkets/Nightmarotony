import pygame
try:
    import const
    import data
except:
    from gamelib import const, data


class State:
    def __init__(self):
      self.state_name = None
      self.shelf_info = pygame.image.load(
          data.filepath("Game", "shelf_info.png"))

    def run_state(self, state_name, real_screen):

        if state_name == 'shelf':
            self.run_shelf_state(real_screen)

    def run_shelf_state(self, real_screen):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        while True:
            self.screen.fill(0)
            self.screen.blit(self.shelf_info, [40, 100])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

