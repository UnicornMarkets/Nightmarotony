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
    from levels import *
except:
    from gamelib import const, data, gifimage
    from gamelib.character import Character
    from gamelib.shelf import Shelf
    from gamelib.state import State
    from gamelib.door import Door
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
        startbar = pygame.image.load(data.filepath("Cover", "startbutton.png"))
        image_num = 0
        num_str = '{0:03}'.format(image_num)
        button = None
        image = pygame.image.load(data.filepath("Cover Image Sequence",
                                                start_string + num_str + ".jpg"))

        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        button = None
        pygame.display.update()

        last_time = pygame.time.get_ticks()
        while not self.start:

            self.screen.blit(image, (0, 0))

            if image_num == 155:
                button = self.screen.blit(startbar, (250, 400))
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
        self.sprites = pygame.sprite.Group()
        self.player = Character(self.sprites)
        self.shelf = Shelf(self.sprites)
        self.door = Door(self.sprites)
        self.grass = pygame.image.load(data.filepath("Game", "grass.png"))

        pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    def loop(self):
        result = None
        while 1:
            self.views()
            if result is None:
                #self.event_processor()
                result = Level(self, level1).loop()
            elif result == 'escape':
                self.finish_game()

    def views(self):
        self.sprites.update(self)
        self.screen.fill(0)
        for x in range(0, 2 * const.WIDTH // self.grass.get_width() + 1):
            for y in range(0, 2 * const.HEIGHT // self.grass.get_height() + 1):
                self.screen.blit(self.grass, (x * 100, y * 100))

        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.shelf.image, self.shelf.rect)
        self.screen.blit(self.door.image, self.door.rect)
        pygame.display.flip()

    def event_processor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                self.player.choose_direction()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.standing()


            if self.player.rect.colliderect(self.shelf.rect):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = State(state_name='shelf')
                    state.run_state(self.real_screen)

            if self.player.rect.colliderect(self.door.rect):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = State(state_name='door')
                    self.result = state.run_state(self.real_screen)

        pygame.display.flip()

    def finish_game(self):
        self.screen = pygame.display.set_mode((700, 700))
        success = pygame.image.load(data.filepath("Cover", "passed.png"))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((255, 255, 255))
            self.screen.blit(success, (200, 250))
            pygame.display.flip()


class Level:
    def __init__(self, game, level):
        self.game = game
        self.window = game.window
        self.real_screen = game.real_screen
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        self.player = game.player
        self.level = level
        self.background = pygame.image.load(data.filepath("Purple Minigame",
                                                "purple map_00000.png"))
        self.sprites = game.sprites
        self.player = Character(self.sprites)
        self.shelf = Shelf(self.sprites)
        self.door = Door(self.sprites)
        self.result = None
        # set up params to determine which level to make

    def map_setup(self):
        #uses the level maps to generate a map that the player walks through

        #TODO: in self.level get all lists and iterate. Create Blocks where true
        pass

    def loop(self):
        # TODO: loop to keep level running
        # TODO: setup a background of purple minigame 0
        while 1:
            self.views()
            self.event_processor()
            if self.result:
                return self.result


    def views(self):
        self.sprites.update(self.game)
        self.screen.fill(0)

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.shelf.image, self.shelf.rect)
        self.screen.blit(self.door.image, self.door.rect)
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
