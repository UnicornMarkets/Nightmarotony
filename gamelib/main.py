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
    player = pygame.image.load("resources/images/person.png")
    while 1:
        screen.fill(0)
        screen.blit(player, playerpos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
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
