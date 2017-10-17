import pygame
import const
import data

class GameWindow(object):

    def __init__(self):
        pygame.display.set_caption('Nightmarotony')
        self.screen = pygame.display.set_mode((2*const.WIDTH, 2*const.HEIGHT))
        try:
            pygame.mixer.init()
        except:
            print 'Cannot load music.'
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
        #self.theme_sound = pygame.mixer.Sound(data.filepath('theme.wav'))
        #self.theme_sound.set_volume(const.SOUND_VOLUME)

    def loop(self):

        startbar = pygame.image.load(data.filepath("Cover", "start_button.png"))
        cover = gifimage.GIFImage(data.filepath("Cover", "nightmarotony cover.gif"))

        pygame.transform.scale(self.screen, (2*const.WIDTH, 2*const.HEIGHT),
                                                            self.real_screen)
        pygame.display.update()

        self.start = False
        while not self.start:

            cover.render(self.screen, (0, 0))
            button = self.screen.blit(startbar, (100, 240))
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
        self.screen = pygame.surface.Surface((const.WIDTH, const.HEIGHT))
        self.clock = pygame.time.Clock()

    def loop(self):
        while 1:
            pass
