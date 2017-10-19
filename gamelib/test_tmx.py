import pyscroll

from game import Level
from testing import TestGameWindow

window = TestGameWindow()

level = Level(window)

level.tmxmap()

map_data = pyscroll.TiledMapData(level.map)

map_layer = pyscroll.BufferedRenderer(map_data, (4000, 4000))
