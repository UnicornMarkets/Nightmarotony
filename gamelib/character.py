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
        self.speed = 55.0
        self.image_turn = 1
        self.block_direction = []
        self.direction = {0:'front',1:'front_right', 2:'right',3:'right_back',
                          4: 'back', 5:'back_left', 6:'left', 7:'left_front'}
        self.move_action = {'front':{} ,'front_right':{} , 'right':{},'right_back':{},
                          'back':{}, 'back_left':{}, 'left':{}, 'left_front':{}}
        self.last_time = pygame.time.get_ticks()
        self.now_direction = 0
        for id in range(1,5):
            self.move_action['front_right'][id] = pygame.transform.scale(pygame.image.load(
                            data.filepath("Game", "nightmarotony sprite -back right-0" + str(id) + ".png")
                                                 ), (50, 100))
            self.move_action['left_front'][id] = pygame.transform.scale(pygame.image.load(data.filepath("Game",
                                                             "nightmarotony sprite -back left-0" + str(
                                                                 id) + ".png")), (50, 100))
        for animate in self.direction.values():
            self.sprite_dict[animate] = pygame.image.load(data.filepath("Game", animate + ".png"))
        self.image = self.sprite_dict['front']
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((320, 370), (image_size[0], image_size[1]))


    def update(self, game):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.now_direction not in self.block_direction:
                self.move(game)
                if self.now_direction == 1 or self.now_direction == 7:
                    self.change_image()

    def change_image(self):
        self.image = self.move_action[self.direction[self.now_direction]][self.image_turn]
        if pygame.time.get_ticks() > self.last_time + 100:
            if (self.image_turn + 1) > 4:
                self.image_turn = 1
            else:
                self.image_turn += 1
            self.last_time = pygame.time.get_ticks()

    def standing(self):
        self.image = self.sprite_dict[self.direction[self.now_direction]]

    def choose_direction(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.change_direction(-1)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.change_direction(1)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.change_direction(4)
        self.image = self.sprite_dict[self.direction[self.now_direction]]

    def change_direction(self, change):
        self.now_direction += change
        if self.now_direction < 0:
            self.now_direction += 8
        elif self.now_direction > 7:
            self.now_direction -= 8

    def move(self, game):
        shelf_rect = game.shelf.rect
        if (self.rect.colliderect(shelf_rect) and self.now_direction not in
            self.block_direction) or not self.rect.colliderect(shelf_rect):
            if self.now_direction == 0:
                self.rect.y -= self.speed * game.dt
                self.check_block(shelf_rect, 0)
            if self.now_direction == 1:
                self.rect.y -= self.speed * game.dt
                self.rect.x += self.speed * game.dt
                self.check_block(shelf_rect, 1)
            if self.now_direction == 2:
                self.rect.x += self.speed * game.dt
                self.check_block(shelf_rect, 2)
            if self.now_direction == 3:
                self.rect.y += sqrt((self.speed ** 2)/2) * game.dt
                self.rect.x += sqrt((self.speed ** 2)/2) * game.dt
                self.check_block(shelf_rect, 3)
            if self.now_direction == 4:
                self.rect.y += self.speed * game.dt
                self.check_block(shelf_rect, 4)
            if self.now_direction == 5:
                self.rect.y += self.speed * game.dt
                self.rect.x -= self.speed * game.dt
                self.check_block(shelf_rect, 5)
            if self.now_direction == 6:
                self.rect.x -= self.speed * game.dt
                self.check_block(shelf_rect, 6)
            if self.now_direction == 7:
                self.rect.y -= self.speed * game.dt
                self.rect.x -= self.speed * game.dt
                self.check_block(shelf_rect, 7)

    def check_block(self, shelf_rect, direction):
        if self.rect.colliderect(shelf_rect):
            if self.block_direction == []:
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
