'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data
import pygame
from pygame.locals import *

def main():
    pygame.init()
    width, height = 800, 600
    keys = {'w': False, 's': False, 'a': False, 'd': False}
    playerpos = [100, 100]
    screen = pygame.display.set_mode((width, height))
    grass = pygame.image.load("resources/images/grass.png")
    player = pygame.image.load("resources/images/person.png")
    shelf = pygame.image.load("resources/images/shelf.png")
    shelf_info = pygame.image.load("resources/images/shelf_info.png")
    while 1:
        screen.fill(0)
        for x in range(0, width // grass.get_width() + 1):
            for y in range(0, height // grass.get_height() + 1):
                screen.blit(grass, (x * 100, y * 100))
        screen.blit(player, playerpos)
        screen.blit(shelf, (0, 30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if playerpos[0] >=-15 and playerpos[0] <=10 and playerpos[1] >=15 and playerpos[1] <=45 \
                                and event.type==pygame.MOUSEBUTTONDOWN:
                screen1 = pygame.display.set_mode((width, height))
                close = 1
                while close:
                    screen1.fill(0)
                    screen1.blit(shelf_info, [40,100])
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            close = 0
            if event.type == pygame.KEYDOWN:
                if event.key == K_w or event.key == K_UP:
                    keys['w'] = True
                elif event.key == K_a or event.key == K_LEFT:
                    keys['a'] = True
                elif event.key == K_s or event.key == K_DOWN:
                    keys['s'] = True
                elif event.key == K_d or event.key == K_RIGHT:
                    keys['d'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == K_UP:
                    keys['w'] = False
                elif event.key == pygame.K_a or event.key == K_LEFT:
                    keys['a'] = False
                elif event.key == pygame.K_s or event.key == K_DOWN:
                    keys['s'] = False
                elif event.key == pygame.K_d or event.key == K_RIGHT:
                    keys['d'] = False
        if keys['w']:
            playerpos[1] -= 1.5
        elif keys['s']:
            playerpos[1] += 1.5
        if keys['a']:
            playerpos[0] -= 1.5
        elif keys['d']:
            playerpos[0] += 1.5
