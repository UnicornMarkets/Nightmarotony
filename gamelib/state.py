import pygame

import yaml
try:
    import const
    import data
except:
    from gamelib import const, data


class State:
    def __init__(self, state_name=None):
        self.state_name = state_name
        self.information = yaml.load(data.filepath("configs", "state.yaml"))


    def run_state(self, real_screen):

        if self.state_name == 'shelf':
            self.run_shelf_state(real_screen)
        if self.state_name == 'door':
            return self.run_door_state(real_screen)

    def run_shelf_state(self, real_screen):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        shelf_info = pygame.image.load(
          data.filepath("Game", "shelf_info.png"))
        while True:
            self.screen.fill(0)
            self.screen.blit(shelf_info, [40, 100])
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
        door_image = {}
        for id in [0,2,4,7]:
            door_image[id] = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "num-" + str(id) +".png")), (40,40))
        button = {}
        correction = [False, False, False, False]
        result = None
        while True:
            self.screen.fill(0)
            for id in [0, 2, 4, 7]:
                button[id] = self.screen.blit(door_image[id], [id*50, 40])
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return True
            if result == 'escape':
                return result
            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def run_door_state1(self, real_screen):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        true_image = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "true.png")), (60, 60))
        false_image = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "false.png")), (60, 60))
        correction = 0
        button = {}
        word = self.change_word()
        result = None
        while True:
            self.screen.fill(0)
            button[0] = self.screen.blit(false_image[id], [50, 40])
            button[1] = self.screen.blit(true_image[id], [100, 40])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[0].collidepoint(position):
                            result = self.check_correct()
                            if result == False:
                                correction += 1
                    word = self.change_word()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[1].collidepoint(position):
                            result = self.check_correct()
                            if result == True:
                                correction += 1
                    word = self.change_word()
            if correction >= 15 :
                return 'escape'

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def check_out(self, correction):
        if False not in correction:
            return 'escape'
        else:
            return None

    def change_word(self):
        """color = {'red':(255, 0, 0), 'green'= (0, 255, 0)
        color_blue = (0, 0, 255)
        fontObj = pygame.font.Font('LOWRBI__.TTF', 32)

        # 创建一个存放文字surface对象，
        textSurfaceObj = fontObj.render(u'HELLO MONCHHICHI', False,
                                        color_green)

        # 文字图像位置
        textRectObj = textSurfaceObj.get_rect()

        # 第二组文字
        fontObj2 = pygame.font.Font('simkai.TTF', 20)"""