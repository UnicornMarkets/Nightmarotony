import pygame
import time
from random import choice
import random
import numpy
import yaml
try:
    import const
    import data
except:
    from gamelib import const, data


class State:
    def __init__(self, level, state_name=None):
        self.level = level
        self.real_screen = level.real_screen
        self.state_name = state_name
        self.information = yaml.load(data.filepath("configs", "state.yaml"))
        self.background = level.background
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.exit_animation = False

    def animation(self, ent_exit, image_num):
        num_str = '{0:03}'.format(image_num)
        last_time = pygame.time.get_ticks()
        self.screen.blit(self.background, (0, 0))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        while not self.exit_animation:

            if pygame.time.get_ticks() > last_time + 5:
                if ent_exit == "enter":
                    image_num += 1
                if ent_exit == "exit":
                    image_num -= 1
                num_str = '{0:03}'.format(image_num)
                self.background = pygame.image.load(data.filepath(self.level.directory,
                                        self.level.bg_color + " map_00" + num_str + ".png"))
                last_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if image_num == 71 or image_num == 0:
                self.exit_animation = True

            self.screen.blit(self.background, (0, 0))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()


    def run_state(self, real_screen):

        return_value = None

        self.animation("enter", 0)
        self.exit_animation = False

        if self.state_name == 'shelf':
            self.run_shelf_state(real_screen)
        if self.state_name == 'door':
            return_value = self.try_out_room(real_screen, [1, 2, 3, 4])

        self.animation("exit", 71)

        return return_value


    def run_shelf_state(self, real_screen):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        word_list = []
        shelf_info = {}
        while len(word_list) < 5:
            new_word = random.randint(0,9)
            if new_word not in word_list:
                word_list += [new_word]
                shelf_info[new_word] = pygame.transform.scale(pygame.image.load(
                    data.filepath("Game", "num-" + str(new_word) + ".png")), (90,50))
        while True:
            self.screen.blit(self.background, (0, 0))
            for y in range(0, 4):
                self.screen.blit(shelf_info[word_list[y]],[y * 100 + 150, 300])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()
            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def try_out_room(self, real_screen, password):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        door_image = {}
        turns = 0
        for id in range(0,10):
            door_image[id] = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "num-" + str(id) +".png")), (90,50))
        button = {}
        correction = [False, False, False, False]
        result = None
        while True:
            self.screen.fill(0)
            self.screen.blit(self.background, (0, 0))
            button[0] = self.screen.blit(door_image[0], [300, 500])
            for id in range (0,3):
                for y in range (0,3):
                    button[y + 1 + id * 3] = self.screen.blit(door_image[y + 1 +  id * 3], [y*100+200, id*100+200])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[password[0]].collidepoint(position):
                            correction[0] = True
                        elif button[password[1]].collidepoint(position) and correction[0]:
                            correction[1] = True
                        elif button[password[2]].collidepoint(position) and correction[1]:
                            correction[2] = True
                        elif button[password[3]].collidepoint(position) and correction[2]:
                            correction[3] = True
                        turns += 1

                if turns >= 4:
                    return self.check_out(correction)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return True
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()
            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def minigame_check_color(self, real_screen):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        true_image = pygame.image.load(data.filepath("Game", "true.png"))
        false_image = pygame.image.load(data.filepath("Game", "false.png"))
        correction = 0
        button = {}
        last_time = pygame.time.get_ticks()
        word, color, sur = self.change_word()
        while True:
            self.screen.fill(0)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(sur, [200, 250])
            button[0] = self.screen.blit(false_image, [300, 200])
            button[1] = self.screen.blit(true_image, [300, 300])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if button[0].collidepoint(position):
                            if self.check_correct(word, color) == False:
                                correction += 1
                        elif button[1].collidepoint(position):
                            if self.check_correct(word, color) == True:
                                correction += 1
                        word, color, sur = self.change_word()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return None
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()
            if correction >= 5 :
                return 70
            if self.check_time(30000, last_time):
                return None

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def check_out(self, correction):
        if False not in correction:
            return 70
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
        fontObj = pygame.font.SysFont('Arial', 45)
        textSurfaceObj = fontObj.render(now_word, False,
                                        color[now_color])
        return now_word, now_color, textSurfaceObj

    def check_correct(self, word, color):
        if word == color:
            return True
        else:
            return False


    def minigame_number_order(self, real_screen):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        turns = 0
        goal_number = 5
        correction = numpy.zeros(goal_number)
        last_word = None
        button = {}
        word_list = []
        word = {}
        last_time = pygame.time.get_ticks()
        pygame.font.init()
        fontObj = pygame.font.SysFont('Arial', 32)
        while len(word_list) < goal_number:
            new_word = random.randint(-99,99)
            if new_word not in word_list:
                word[new_word] = fontObj.render(str(new_word), False,(255, 0, 0))
                word_list += [new_word]
        while True:
            self.screen.blit(self.background, (0, 0))
            for x in range(0, len(word_list)):
                button[x] = self.screen.blit(word[word_list[x]], [320, 240+x*40])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        for x in range(0, len(word_list)):
                            if button[x].collidepoint(position):
                                if last_word == None or word_list[x] > last_word:
                                    correction[turns] = 1
                                last_word = word_list[x]
                        turns += 1

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return None
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()
            if turns >= goal_number :
                if 0 not in correction:
                    return 70
                else:
                    return -200

            if self.check_time(30000, last_time):
                return None

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   real_screen)

    def check_time(self, tick, last_time):
        if pygame.time.get_ticks() > last_time + tick:
            return True
        else:
            return False
