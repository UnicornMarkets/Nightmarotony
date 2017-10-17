import pygame
from math import sqrt
try:
    from gamelib import data
except:
    import data

class Character(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Character, self).__init__(*groups)
        self.sprite_dict = {}
        self.speed = 35
        self.block_direction = []
        self.direction = {0:'front',1:'front_right', 2:'right',3:'right_back',
                          4: 'back', 5:'back_left', 6:'left', 7:'left_front'}
        self.now_direction = 0
        for animate in self.direction.values():
            self.sprite_dict[animate] = pygame.image.load(data.filepath("Game", animate + ".png"))
        self.image = self.sprite_dict['front']
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((320, 370), (image_size[0] / 2, image_size[1] / 2))


    def update(self, game):

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.change_direction(-1)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.change_direction(1)
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.now_direction not in self.block_direction:
                self.move(game.shelf.rect)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.change_direction(4)
        self.image = self.sprite_dict[self.direction[self.now_direction]]

    def change_direction(self, change):
        self.now_direction += change
        if self.now_direction < 0:
            self.now_direction += 8
        elif self.now_direction > 7:
            self.now_direction -= 8

    def move(self, shelf_rect):
        if self.now_direction == 0:
            self.rect.y -= self.speed
            self.check_block(shelf_rect, 0)
        if self.now_direction == 1:
            self.rect.y -= sqrt((self.speed ^ 2) / 2)
            self.rect.x += sqrt((self.speed ^ 2) / 2)
            self.check_block(shelf_rect, 1)
        if self.now_direction == 2:
            self.rect.x += self.speed
            self.check_block(shelf_rect, 2)
        if self.now_direction == 3:
            self.rect.y += sqrt((self.speed ^ 2) / 2)
            self.rect.x += sqrt((self.speed ^ 2) / 2)
            self.check_block(shelf_rect, 3)
        if self.now_direction == 4:
            self.rect.y += self.speed
            self.check_block(shelf_rect, 4)
        if self.now_direction == 5:
            self.rect.y += sqrt((self.speed ^ 2) / 2)
            self.rect.x -= sqrt((self.speed ^ 2) / 2)
            self.check_block(shelf_rect, 5)
        if self.now_direction == 6:
            self.rect.x -= self.speed
            self.check_block(shelf_rect, 6)
        if self.now_direction == 7:
            self.rect.y -= sqrt((self.speed ^ 2) / 2)
            self.rect.x -= sqrt((self.speed ^ 2) / 2)
            self.check_block(shelf_rect, 7)

    def check_block(self, shelf_rect, direction):
        if self.rect.colliderect(shelf_rect):

            self.block_direction += [direction]
            if direction - 1 < 0:
                self.block_direction += [direction + 7]
            else:
                self.block_direction += [direction - 1]
            if direction + 1 > 7:
                self.block_direction += [direction - 7]
            else:
                self.block_direction += [direction + 1]
        else:
            self.block_direction = []
