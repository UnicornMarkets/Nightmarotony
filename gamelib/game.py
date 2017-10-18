import pygame
import sys
try:
    import const
    import data
    import gifimage
    from character import Character
    from shelf import Shelf
    from state import State
except:
    from gamelib import const, data, gifimage
    from gamelib.character import Character
    from gamelib.shelf import Shelf
    from gamelib.state import State

import pytmx
from pytmx.util_pygame import load_pygame

class GameWindow(object):

    def __init__(self):
        pygame.display.set_caption('Nightmarotony')
        self.screen = pygame.display.set_mode((2*const.WIDTH, 2*const.HEIGHT))

        try:
            pygame.mixer.init()
        except:
            pass
        self.intro()

    def intro(self):

        start = Intro(self).loop()
        if start:
            self.game()

    def game(self):
        Game(self).loop()

class Intro(object):

    def __init__(self, window):
        self.window = window
        self.real_screen = window.screen
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        #self.select_sound = pygame.mixer.Sound(data.filepath('click_mouse.wav'))
        #self.select_sound.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.load(data.filepath('Audio', 'welcome.mp3'))
        pygame.mixer.music.play()

    def loop(self):

        startbar = pygame.image.load(data.filepath("Cover", "start_button.png"))
        cover = gifimage.GIFImage(data.filepath("Cover", "nightmarotony cover.gif"))

        pygame.transform.scale(self.screen, (2*const.WIDTH, 2*const.HEIGHT),
                                                            self.real_screen)
        pygame.display.update()

        self.start = False
        while not self.start:

            cover.render(self.screen, (0, 0))
            button = self.screen.blit(startbar, (120, 100))
            pygame.transform.scale(self.screen, (2*const.WIDTH, 2*const.HEIGHT),
                                                               self.real_screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    self.on_start(event, button)
        return self.start

    def on_start(self, event, button):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self.start = True
                #self.select_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = pygame.mouse.get_pos()
                if button.collidepoint(position):
                    self.start = True
                    #self.select_sound.play()

class Game(object):

    def __init__(self, window):
        self.window = window
        self.real_screen = window.screen
        self.state = State()
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.player = Character(self.sprites)
        self.shelf = Shelf((self.sprites))
        self.grass = pygame.image.load(data.filepath("Game", "grass.png"))
        self.map = load_pygame("Tilemap/tmx/Dungeon.tmx")

    def tmxmap(self):
        print self.map

    def loop(self):
        print self.map
        #props = self.get_tile_properties(x, y, layer)
        print self.map.properties, 'property'
        print self.map.layers, 'layer'
        for layer in self.map.visible_layers:
            print layer
        layer1 = self.map.get_layer_by_name("Tile Layer 1")
        print layer1
        object = self.map.objects
        print self.map.objectgroups, 'object group'


        print 123213213123
        while 1:
            self.views()
            self.event_processor()

    def views(self):
        self.screen.fill(0)
        for x in range(0, 2 * const.WIDTH // self.grass.get_width() + 1):
            for y in range(0, 2 * const.HEIGHT // self.grass.get_height() + 1):
                self.screen.blit(self.grass, (x * 100, y * 100))

        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.shelf.image, self.shelf.rect)
        pygame.display.flip()

    def event_processor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                self.player.update(self)

            if self.player.rect.colliderect(self.shelf.rect):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.run_state('shelf', self.real_screen)
        self.screen.blit(self.screen, (0, 0))
        pygame.transform.scale(self.screen,
                               (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()