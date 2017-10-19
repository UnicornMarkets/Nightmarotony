import pygame
import tmx
import pytmx
from pytmx.util_pygame import load_pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('data/Game/lichking.png'),
                                       (100, 100))
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

        # gravity
        #self.resting = False
        #self.dy = 0

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
        """
        # GRAVITY
        if self.resting and key[pygame.K_SPACE]:
            self.dy = -500
        self.dy = min(400, self.dy + 40)

        self.rect.y += self.dy * dt

        """
        if key[pygame.K_UP]:
            self.rect.y -= 300 * dt
        if key[pygame.K_DOWN]:
            self.rect.y += 300 * dt

        new = self.rect

        #self.resting = False

        for cell in pygame.sprite.spritecollide(self, game.walls, False):
            cell = cell.rect
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True

                new.bottom = cell.top
                self.dy = 0

            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0



class Game:
    def main(self, screen):

        clock = pygame.time.Clock()

        background = pygame.transform.scale(pygame.image.load(
            'data/Game/map.png'),
                                            (1024, 1024))

        sprites = pygame.sprite.Group()
        self.player = Player(sprites)

        self.walls = pygame.sprite.Group()
        block = pygame.transform.scale(pygame.image.load(
            'data/Game/block.png'), (32, 32))
        for x in range(0, 1024, 32):
            for y in range(0, 1024, 32):
                #if x in (0, 1024-32) or y in (0, 1024-32):
                if x == 32 and y == 32:

                    wall = pygame.sprite.Sprite(self.walls)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x,y), block.get_size())
        sprites.add(self.walls)



        #self.tilemap = load_pygame("Dungeon.tmx")

        #self.tilemap = tmx.TileMap.load('Dungeon.tmx')
        #start_cell = self.tilemap.layers['triggers'].find('player')[0]
        #self.player = Player((start_cell.px, start_cell.py), self.sprites)
        #self.tilemap.layers.append(self.sprites)



        while 1:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == \
                        pygame.K_ESCAPE:
                    return
            sprites.update(dt / 1000.0, self)
            #self.tilemap.update(dt / 1000.0, self)

            screen.blit(background, (0, 0))
            sprites.draw(screen)
            #self.tilemap.draw(screen)
            pygame.display.flip()

#if __name__ == '__main__':
def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    Game().main(screen)