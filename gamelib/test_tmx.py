import pyscroll

import pygame
from game import Level
from testing import TestGameWindow
from character import Character

group = pygame.sprite.Group()

sprite = Character(group)

window = TestGameWindow()

level = Level(window, sprite)

level.tmxmap()

level.loop()

#map_data = pyscroll.TiledMapData(level.map)

#map_layer = pyscroll.BufferedRenderer(map_data, (4000, 4000))

#group = pyscroll.PyscrollGroup(map_layer=map_layer)

sprite = Character(group)

#group.center(sprite.rect.center)
