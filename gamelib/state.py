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
    def __init__(self, level, state_name):
        self.level = level
        self.real_screen = level.real_screen
        self.state_name = state_name
        self.information = yaml.load(data.filepath("configs", "state.yaml"))
        self.background = level.background
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.exit_animation = False
        self.pin = level.pin
        pygame.mixer.music.stop()
        pygame.mixer.music.load(data.filepath('Audio', 'mini_2.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    def animation(self, ent_exit, image_num):
        num_str = '{0:03}'.format(image_num)
        last_time = pygame.time.get_ticks()
        self.screen.blit(self.background, (0, 0))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        while not self.exit_animation:


            if ent_exit == "enter":
                image_num += 1
            if ent_exit == "exit":
                image_num -= 1
            num_str = '{0:03}'.format(image_num)
            self.background = pygame.image.load(data.filepath(self.level.directory,
                                    self.level.bg_color + " map_00" + num_str + ".png"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if image_num == 71 or image_num == 0:
                self.exit_animation = True

            self.screen.blit(self.background, (0, 0))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()


    def run_state(self):

        return_value = None
        play_time = 24000 - 2000 * self.level.game_level
        goal_number = 2 * self.level.game_level

        self.animation("enter", 0)
        self.exit_animation = False

        if self.state_name == 'shelf':
            self.run_shelf_state()
        if self.state_name == 'computer':
            self.minigame_check_color(play_time)
        if self.state_name == 'phone':
            self.minigame_number_order(play_time, goal_number)
        if self.state_name == 'door':
            return_value = self.try_out_room()

        self.animation("exit", 71)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

        return return_value

    def run_shelf_state(self):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        shelf_info = {}
        for num in self.pin:
            shelf_info[num] = pygame.transform.scale(pygame.image.load(
                    data.filepath("Game", "num-" + str(num) + ".png")), (90,50))

        text_screen = """Do your homework Tony! Then you can get the pin. \n
                       Don't forget to match the colors to words, read your \n
                       emails, and order all the numbers on your phone"""
        pygame.font.init()
        fontObj = pygame.font.SysFont('Arial', 75)
        textSurfaceObj = fontObj.render(text_screen, False,
                                        (255, 255, 255))
        while True:

            if self.level.reading_flag and self.level.sequence_flag and self.level.color_flag:
                for y in range(0, 4):
                    self.screen.blit(shelf_info[self.pin[y]],
                                               [y * 100 + 150, 300])
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
                            self.screen.blit(self.background, (0, 0))
                pygame.transform.scale(self.screen,
                                       (2 * const.WIDTH, 2 * const.HEIGHT),
                                       self.real_screen)
            else:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(textSurfaceObj, (200, 250))
                pygame.transform.scale(self.screen,
                                       (2 * const.WIDTH, 2 * const.HEIGHT),
                                       self.real_screen)

    def try_out_room(self):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        door_image = {}
        turns = 0
        for num in range(0, 10):
            door_image[num] = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "num-" + str(num) +".png")), (90,50))
        button = {}
        correction = []
        result = None
        while True:
            self.screen.fill(0)
            self.screen.blit(self.background, (0, 0))
            button[0] = self.screen.blit(door_image[0], [300, 500])
            for num in range (0,3):
                for y in range (0,3):
                    button[y + 1 + num * 3] = self.screen.blit(door_image[y + 1 +  num * 3],
                                                              [y*100+200, num*100+200])

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    position = pygame.mouse.get_pos()
                    for key, butt in button.items():
                        if butt.collidepoint(position):
                            correction.append(key)
                    turns += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return

                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

            if turns >= 4:
                return self.check_out(correction)


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

    def minigame_check_color(self, play_time):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        true_image = pygame.transform.scale(pygame.image.load(data.filepath("Game", "true.png")),
                                            (150, 65))
        false_image = pygame.transform.scale(pygame.image.load(data.filepath("Game", "false.png")),
                                            (150, 65))
        trials = 0
        correction = 0
        button = {}
        last_time = pygame.time.get_ticks()
        word, color, sur = self.change_word()
        while True:
            self.screen.fill(0)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(sur, [300, 200])
            button[False] = self.screen.blit(false_image, [200, 320])
            button[True] = self.screen.blit(true_image, [400, 320])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        for key, butt in button.items():
                            if butt.collidepoint(position):
                                if key == self.check_correct(word, color):
                                    correction += 1
                                word, color, sur = self.change_word()
                                trials += 1


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

            if trials >= 5:
                if correction >= 5:
                    self.level.color_flag = True
                    return
                else:
                    return

            if self.check_time(play_time, last_time):
                return

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)

    def check_out(self, correction):
        if correction == self.pin:
            return random.randint(1, 12)
        else:
            return -1

    def change_word(self):
        color_red = (255, 0, 0)
        color_green = (0, 255, 0)
        color_blue = (0, 0, 255)
        color = {'red': color_red, 'green': color_green, 'blue': color_blue}
        word = ['red', 'green', 'blue']
        now_color = choice(list(color.keys()))
        now_word = choice(word)
        pygame.font.init()
        fontObj = pygame.font.SysFont('Arial', 75)
        textSurfaceObj = fontObj.render(now_word, False,
                                        color[now_color])
        return now_word, now_color, textSurfaceObj

    def check_correct(self, word, color):
        if word == color:
            return True
        else:
            return False


    def minigame_number_order(self, play_time, goal_n):
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
            new_word = random.randint(-99, 99)
            if new_word not in word_list:
                word[new_word] = fontObj.render(str(new_word), False, (255, 0, 0))
                word_list += [new_word]
        while True:
            self.screen.blit(self.background, (0, 0))
            for x in range(0, len(word_list)):
                button[x] = self.screen.blit(word[word_list[x]], [320, 240 + x * 40])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        for x in range(0, len(word_list)):
                            if button[x].collidepoint(position):
                                if last_word is None or word_list[x] > last_word:
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
            if turns >= goal_number:
                if 0 not in correction:
                    self.level.sequence_flag = True
                    return
                else:
                    return

            if self.check_time(30000, last_time):
                return None

            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)

    def check_time(self, tick, last_time):
        if pygame.time.get_ticks() > last_time + tick:
            return True
        else:
            return False
