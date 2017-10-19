# This file is so we can run certain segments of code independent of main
from gifimage import GIFImage
from game import Game
from data import filepath
import pygame
import time

class TestGame:

    def __init__(self):
        pygame.init()

    def plain(self, test):
        self.screen = pygame.display.set_mode((200, 200))
        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if test:
                    pygame.time.set_timer(pygame.QUIT, 100)

            self.screen.fill((210, 100, 230))
            pygame.display.flip()

    def gif(self, test):
        self.screen = pygame.display.set_mode((500, 1000))
        cover = GIFImage(filepath("Cover", "nightmarotony cover.gif"))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if test:
                    pygame.time.set_timer(pygame.QUIT, 800)


            self.screen.fill((0,0,0))
            cover.render(self.screen, (0, 0))
            pygame.display.flip()

    def level1(self, test):
        self.screen = pygame.display.set_mode((700, 700))

        Game(self).loop()

    def success(self):
        self.screen = pygame.display.set_mode((700, 700))
        success = pygame.image.load(filepath("Cover", "passed.png"))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((255, 255, 255))
            self.screen.blit(success, (200,250))
            pygame.display.flip()


if __name__ == "__main__":
    try:
        game = TestGame()
        game.plain(True)
        game = TestGame()
        game.gif(True)
        game = TestGame()
        game.level(True)
        game = TestGame()
        game.success()
    except Exception as e:
        print("tests failed")
        print(e)
