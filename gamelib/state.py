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
        self.door_image = {}
        for id in [0,2,4,7]:
            self.door_image[id] = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "num-" + str(id) +".png")), (40,40))

    def run_state(self, state_name, real_screen):

        if state_name == 'shelf':
            self.run_shelf_state(real_screen)
        if state_name == 'door':
            return self.run_door_state(real_screen)

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

    def run_door_state(self, real_screen):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        button = {}
        correction = [False, False, False, False]
        result = None
        while True:
            self.screen.fill(0)
            for id in [0, 2, 4, 7]:
                button[id] = self.screen.blit(self.door_image[id], [id*50, 40])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[2].collidepoint(position):
                            correction[0] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[4].collidepoint(position) and correction[0]:
                            correction[1] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[0].collidepoint(position) and correction[1]:
                            correction[2] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[7].collidepoint(position) and correction[2]:
                            correction[3] = True
                            result = self.check_out(correction)
            if result == 'escape':
                return result


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return True
            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def check_out(self, correction):
        if False not in correction:
            return 'escape'
        else:
            return None
