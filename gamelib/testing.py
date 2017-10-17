# This file is so we can run certain segments of code independent of main
from gifimage import GIFImage
from data import filepath
import pygame

class TestGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 1000))
        self.gif()

    def gif(self):

        cover = GIFImage(filepath("nightmarotony cover.gif"))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0,0,0))
            cover.render(self.screen, (0, 0))
            pygame.display.flip()
