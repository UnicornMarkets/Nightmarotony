import pygame
import sys
import os
import random
import copy

try:
    import const
    import data
    import gifimage
    from character import Character
    from objects import Shelf, Door, Block, VRgoggles, Computer
    from state import State
    from levels import level_dict, corner_dict
except:
    from gamelib import const, data, gifimage
    from gamelib.character import Character
    from gamelib.objects import Shelf, Door, Block
    from gamelib.state import State
    from gamelib.levels import level_dict, corner_dict

class GameWindow(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(45) / 300.0
        pygame.display.set_caption('Nightmarotony')
        self.real_screen = pygame.display.set_mode((2 * const.WIDTH, 2 * const.HEIGHT))

        try:
            pygame.mixer.init()
        except:
            pass
        self.intro()

    def intro(self):
        start = Intro(self).loop()
        if start:
            self.transition()

    def transition(self):
        move_on = Transition(self).loop('intro.png', "transition.wav")
        if move_on:
            self.game()

    def game(self):
        Game(self).loop()


class Intro(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = window.clock
        pygame.mixer.music.load(data.filepath('Audio', 'welcome.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)
        self.start = False

    def loop(self):

        start_string = "nightmarotony cover_00"
        startbar = pygame.transform.scale(pygame.image.load(data.filepath("Cover",
                                                    "startbutton.png")), (118, 59))
        image_num = 0
        num_str = '{0:03}'.format(image_num)
        button = None
        image = pygame.image.load(data.filepath("Cover Image Sequence",
                                                start_string + num_str + ".jpg"))

        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.update()

        last_time = pygame.time.get_ticks()
        while not self.start:

            self.screen.blit(image, (0, 0))

            if image_num == 155:
                button = self.screen.blit(startbar, (300, 400))
            elif pygame.time.get_ticks() > last_time + 20:
                image_num += 1
                num_str = '{0:03}'.format(image_num)
                image = pygame.image.load(data.filepath("Cover Image Sequence",
                                                        start_string + num_str + ".jpg"))
                last_time = pygame.time.get_ticks()

            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if image_num == 155 and button:
                    self.on_start(event, button)

        return self.start

    def on_start(self, event, button):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
           (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
            button.collidepoint(pygame.mouse.get_pos())):
                self.start = True
                startsound = pygame.mixer.Sound(data.filepath('Audio', 'start.wav'))
                startsound.set_volume(const.SOUND_VOLUME / 3)
                startsound.play()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

class Transition(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.move_on = False

    def loop(self, filename, audio_file):
        img = pygame.image.load(data.filepath("Transitions", filename))
        img = pygame.transform.scale(img, (700, 700))
        click = pygame.image.load(data.filepath("Transitions", "click.png"))


        self.screen.blit(img, (0, 0))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
        pygame.mixer.music.load(data.filepath("Audio", audio_file))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME / 8)
        pygame.mixer.music.play(-1)
        click_time = pygame.time.get_ticks()

        while not self.move_on:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    elif event.key == pygame.K_SPACE:
                        self.move_on = True

                elif event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.move_on = True

            if self.move_on is True:
                pygame.mixer.music.stop()

            self.screen.blit(img, (0, 0))
            if pygame.time.get_ticks() >= click_time + const.FADEOUT_TIME:
                self.screen.blit(click, (340, 580))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

        return self.move_on


class Game(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = window.clock
        self.dt = window.dt

    def loop(self):
        level_num = 1
        game_level = 1
        color_list = ['blue', 'green', 'purple']

        while 1:
            color = random.choice(color_list)
            if level_num > 0 and level_num <= 70 and game_level <= 8:
                pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME)
                pygame.mixer.music.play(-1)

                level_str = "level_" + str(level_num)
                result = Level(self, level_str, level_num, color).loop()

                transition_str = 'transition_' + str(game_level) + '.png'
                move_on = Transition(self).loop(transition_str, "transition.wav")
                level_num += result
                game_level += 1

            elif level_num <= 0:
                pygame.mixer.music.load(data.filepath('Audio', 'lose.wav'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME / 2)
                pygame.mixer.music.play(-1)
                self.lose_game()

            elif game_level > 8 or level_num > 70:
                pygame.mixer.music.load(data.filepath('Audio', 'win.wav'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME / 2)
                pygame.mixer.music.play(-1)
                self.win_game()

    def win_game(self):
        start_string = "YOU WON_00"
        directory = "End Sequence YOU WON"
        image_count = 215

        self.animate(start_string, directory, image_count)

        self.window.game()

    def lose_game(self):
        start_string = "YOU LOST_00"
        directory = "End Sequence YOU LOST"
        image_count = 215

        self.animate(start_string, directory, image_count)

        self.window.game()

    def animate(self, start_string, directory, image_count):
        restartbar = pygame.transform.scale(pygame.image.load(data.filepath("Cover",
                                                      "restart-01.png")), (118, 59))
        image_num = 0
        num_str = '{0:03}'.format(image_num)
        button = None
        image = pygame.image.load(data.filepath(directory,
                                            start_string + num_str + ".png"))

        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.update()

        last_time = pygame.time.get_ticks()
        restart = False
        while not restart:

            self.screen.blit(image, (0, 0))

            if image_num == image_count:
                button = self.screen.blit(restartbar, (500, 600))
            elif pygame.time.get_ticks() > last_time + 20:
                image_num += 1
                num_str = '{0:03}'.format(image_num)
                image = pygame.image.load(data.filepath(directory,
                                                start_string + num_str + ".png"))
                last_time = pygame.time.get_ticks()

            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()

                if image_num == image_count and button:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position = pygame.mouse.get_pos()
                            if button.collidepoint(position):
                                restart = True

class ScrolledGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x - self.camera_x,
                                        sprite.rect.y - self.camera_y))

class Level:
    def __init__(self, game, level_string, level_number, bg_color):
        if bg_color == 'blue':
            self.directory = 'Blue Minigame'
        elif bg_color == 'purple':
            self.directory = 'Purple Minigame'
        elif bg_color == 'green':
            self.directory = 'Green Minigame'
        elif bg_color == 'red':
            self.directory = 'Red Minigame'
        self.bg_color = bg_color
        self.level_number = level_number
        self.game = game
        self.window = game.window
        self.real_screen = game.real_screen
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        self.level = level_dict[level_string]
        self.corners = copy.deepcopy(corner_dict[level_string])
        random.shuffle(self.corners)
        self.background = pygame.image.load(data.filepath(self.directory,
                                            self.bg_color + " map_00000.png"))
        self.dt = game.dt
        self.result = None
        self.sprites = ScrolledGroup()
        self.objects = [Door, Shelf, VRgoggles, Computer]
        self.pin_code = [random.randint(0, 9) for _ in range(4)]

    def player_setup(self):
        self.sprites.camera_x = 0
        self.sprites.camera_y = 0
        x, y = self.corners.pop()
        self.player = Character(x * const.BLOCK_SIZE, y * const.BLOCK_SIZE,
                                self.sprites)

    def object_setup(self):
        # add objects into the map_
        self.object_group = pygame.sprite.Group()
        for thing in self.objects:
            x, y = self.corners.pop()
            trinket = thing(x * const.BLOCK_SIZE, y * const.BLOCK_SIZE,
                            self.pin_code, self.object_group)
        self.sprites.add(self.object_group)

    def map_setup(self):
        tile_colors = ['pink', 'navy', 'purple', 'blue']
        tile_color = random.choice(tile_colors)

        self.walls = pygame.sprite.Group()
        num_row = len(self.level)
        num_col = len(self.level[0])

        for row in range(num_row):
            for col in range(num_col):
                if self.level[row][col] == True:
                    Block(row * const.BLOCK_SIZE, col * const.BLOCK_SIZE,
                       const.BLOCK_SIZE, tile_color, self.walls)
        self.sprites.add(self.walls)
        #uses the level maps to generate a map that the player walks through

    def loop(self):
        self.player_setup()
        self.map_setup()
        self.object_setup()
        while 1:
            self.views()
            self.event_processor()
            if self.result:
                return self.result

    def views(self):
        self.sprites.update(self)
        if self.result:
            return

        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)

        pygame.transform.scale(self.screen,
                               (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

    def event_processor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                self.player.choose_direction()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.standing()

    def transition(self, message):
        obj_str = 'object_' + message + '.png'
        move_on = Transition(self).loop(obj_str, "mini_1.wav")
        if move_on:
            pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
            pygame.mixer.music.set_volume(const.SOUND_VOLUME)
            pygame.mixer.music.play(-1)
