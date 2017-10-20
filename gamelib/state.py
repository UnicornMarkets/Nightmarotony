import pygame
import time
from random import choice
import yaml
try:
    import const
    import data
except:
    from gamelib import const, data


class State:
    def __init__(self, level, state_name=None):
        self.real_screen = level.real_screen
        self.state_name = state_name
        self.information = yaml.load(data.filepath("configs", "state.yaml"))
        self.background = level.background
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.start = False

    def animation(self, ent_exit, image_num):
        num_str = '{0:03}'.format(image_num)
        last_time = pygame.time.get_ticks()
        self.screen.blit(self.background, (0, 0))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        while not self.start:

            if pygame.time.get_ticks() > last_time + 5:
                if ent_exit == "enter":
                    image_num += 1
                if ent_exit == "exit":
                    image_num -= 1
                num_str = '{0:03}'.format(image_num)
                self.background = pygame.image.load(data.filepath("Purple Minigame",
                                            "purple map_00" + num_str + ".png"))
                last_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if image_num == 71:
                self.start = True

            self.screen.blit(self.background, (0, 0))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()


    def run_state(self, real_screen):
        
        return_value = None

        self.animation("enter", 0)

        if self.state_name == 'shelf':
            self.run_shelf_state(real_screen)
        if self.state_name == 'door':
            return_value = self.run_door_state1(real_screen)

        self.animation("exit", 71)

        return return_value

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
        clock = time.time()
        true_image = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "true.png")), (80, 80))
        false_image = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "false.png")), (80, 80))
        correction = 0
        button = {}
        word, color, sur = self.change_word()
        while True:
            self.screen.fill(0)
            self.screen.blit(sur, [150, 20])
            button[0] = self.screen.blit(false_image, [200, 80])
            button[1] = self.screen.blit(true_image, [50, 80])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[0].collidepoint(position):
                            if self.check_correct(word, color) == False:
                                correction += 1
                        word, color, sur = self.change_word()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[1].collidepoint(position):
                            if self.check_correct(word, color) == True:
                                correction += 1
                        word, color, sur = self.change_word()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return None
            if correction >= 5 :
                return 'escape'
            if time.time()-clock >= 30:
                return None

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def check_out(self, correction):
        if False not in correction:
            return 'escape'
        else:
            return None

    def change_word(self):
        color_red = (255, 0, 0)
        color_green = (0, 255, 0)
        color_blue = (0, 0, 255)
        color = {'red':color_red, 'green':color_green, 'blue':color_blue}
        word = ['red', 'green', 'blue']
        now_color = choice(list(color.keys()))
        now_word = choice(word)
        pygame.font.init()
        fontObj = pygame.font.SysFont('Arial', 32)
        textSurfaceObj = fontObj.render(now_word, False,
                                        color[now_color])
        return now_word, now_color, textSurfaceObj

    def check_correct(self, word, color):
        if word == color:
            return True
        else:
            return False
