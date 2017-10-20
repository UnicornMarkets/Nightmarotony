import pygame
import sys
import os

try:
    import const
    import data
    import gifimage
    from character import Character
    from shelf import Shelf
    from door import Door
    from state import State
    from block import Block
    from levels import *
except:
    from gamelib import const, data, gifimage
    from gamelib.character import Character
    from gamelib.shelf import Shelf
    from gamelib.state import State
    from gamelib.door import Door
    from gamelib.block import Block
    from gamelib.levels import *

class GameWindow(object):
    def __init__(self):
        pygame.display.set_caption('Nightmarotony')
        self.screen = pygame.display.set_mode((2 * const.WIDTH, 2 * const.HEIGHT))

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
        move_on = Transition(self).loop()

        if move_on:
            self.game()

    def game(self):
        Game(self).loop()


class Transition(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.move_on = False

    def loop(self):

        intro = pygame.image.load(data.filepath("Cover", "intro.png"))
        intro_scaled = pygame.transform.scale(intro, (700, 700))

        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
        start_time = pygame.time.get_ticks()

        while not self.move_on:
            if pygame.time.get_ticks() >= start_time + const.FADEOUT_TIME:
                intro = pygame.image.load(data.filepath("Cover", "intro-2.png"))
                intro_scaled = pygame.transform.scale(intro, (700, 700))

            pygame.display.update()
            self.screen.fill(0)
            self.screen.blit(intro_scaled, (0, 0))

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

            self.screen.blit(self.screen, (0, 0))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

        return self.move_on


class Intro(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self.start = True
                startsound = pygame.mixer.Sound(data.filepath('Audio', 'start.wav'))
                startsound.set_volume(const.SOUND_VOLUME)
                startsound.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = pygame.mouse.get_pos()
                if button.collidepoint(position):
                    self.start = True
                    startsound = pygame.mixer.Sound(data.filepath('Audio', 'start.wav'))
                    startsound.set_volume(const.SOUND_VOLUME)
                    startsound.play()


class Game(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(30) / 1000.0

        pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    def loop(self):
        level_num = 1
        while 1:
            if level_num > 0 and level_num <= 70:
                level_string = "level" + str(level_num)
                result = Level(self, level_string).loop()
                level_num += result
            elif level_num > 70:
                self.win_game()
            elif level_num <= 0:
                self.lose_game()

    def win_game(self):
        start_string = "Comp 2_00"
        directory = "Ending Sequence"
        image_count = 119

        self.animate(start_string, directory, image_count)

        self.loop()

    def lose_game(self):
        start_string = "YOU LOST_00"
        directory = "End Sequence YOU LOST"
        image_count = 215

        self.animate(start_string, directory, image_count)

        self.loop()

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
    def __init__(self, game, level_string):
        self.game = game
        self.window = game.window
        self.real_screen = game.real_screen
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        self.level = eval(level_string)
        self.dt = game.dt
        self.background = pygame.image.load(data.filepath("Purple Minigame",
                                                      "purple map_00000.png"))
        self.result = None
        self.sprites = pygame.sprite.Group()

    def player_setup(self):
        self.player_sprite = ScrolledGroup()
        self.player_sprite.camera_x = 0
        self.player_sprite.camera_y = 0
        self.player = Character(self.player_sprite)
        self.sprites.add(self.player_sprite)

    def object_setup(self):
        # add objects into the map_
        self.objects = pygame.sprite.Group()
        self.shelf = Shelf(self.objects)
        self.door = Door(self.objects)
        self.sprites.add(self.objects)

    def map_setup(self):

        self.walls = pygame.sprite.Group()
        num_row = len(self.level)
        num_col = len(self.level[0])

        for row in range(num_row):
            for col in range(num_col):
                if self.level[row][col] == True:
                    Block(row * const.BLOCK_SIZE, col * const.BLOCK_SIZE,
                                const.BLOCK_SIZE, self.walls, self.sprites)

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

        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)

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

            if self.player.rect.colliderect(self.shelf.rect):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = State(self, state_name='shelf')
                    state.run_state(self.real_screen)

            if self.player.rect.colliderect(self.door.rect):
                if event.type == pygame.MOUSEBUTTONDOWN:

                    state = State(self, state_name='door')
                    self.result = state.run_state(self.real_screen)
