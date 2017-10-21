import pygame
from math import sqrt
try:
    from gamelib import data
    from gamelib import const
except:
    import data
    import const

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Character, self).__init__(*groups)
        self.sprite_dict = {}
        self.speed = const.SPEED
        self.image_turn = 1
        self.block_direction = []
        pic_name_lead = "nightmarotony sprite-"
        self.direction = {0:'back', 1:'back right', 2:'right', 3:'front right',
                          4: 'front', 5:'front left', 6:'left', 7:'back left'}
        self.move_action = {'front':{} , 'back right':{} , 'right':{},'front right':{},
                          'back':{}, 'front left':{}, 'left':{}, 'back left':{}}
        self.last_time = pygame.time.get_ticks()
        self.now_direction = 4
        for direct in self.direction.values():
            for num in range(1,5):
                file_name = pic_name_lead + direct + "-0" + str(num) + ".png"
                image = pygame.image.load(data.filepath("Character", file_name))
                scaled_image = pygame.transform.scale(image, (const.CHAR_WIDTH,
                                                              const.CHAR_HEIGHT))
                self.move_action[direct][num] = scaled_image
            self.sprite_dict[direct] = scaled_image

        self.image = self.sprite_dict['front']
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((x, y), (const.CHAR_WIDTH, const.CHAR_HEIGHT))
        # TODO, make rect only on feet


    def update(self, level):
        last = self.rect.copy()
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            if self.now_direction not in self.block_direction:
                self.move(level)
                self.change_image()

        for cell in pygame.sprite.spritecollide(self, level.walls, False):
            cell = cell.rect
            if last.right <= cell.left:
                self.rect.right = cell.left
            if last.left >= cell.right:
                self.rect.left = cell.right
            if last.bottom <= cell.top:
                self.rect.bottom = cell.top
            if last.top >= cell.bottom:
                self.rect.top = cell.bottom

        for pg_object in pygame.sprite.spritecollide(self, level.object_group, False):
            if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                pg_object.start_game(level)
            if last.right <= pg_object.rect.left + 5:
                self.rect.right = pg_object.rect.left + 5
            if last.left >= pg_object.rect.right - 5:
                self.rect.left = pg_object.rect.right - 5
            if last.bottom <= pg_object.rect.top + 5:
                self.rect.bottom = pg_object.rect.top + 5
            if last.top >= pg_object.rect.bottom - 5:
                self.rect.top = pg_object.rect.bottom - 5
            # use space bar to search object for minigame or level exit

        # set the camera to put the player in the middle of the screen
        self.groups()[0].camera_x = self.rect.x - (const.WIDTH - 0.5 * const.CHAR_WIDTH)
        self.groups()[0].camera_y = self.rect.y - (const.HEIGHT - 0.5 * const.CHAR_HEIGHT)

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

    def move(self, level):
        if self.now_direction == 0:
            self.rect.y -= self.speed * level.dt
        if self.now_direction == 1:
            self.rect.y -= sqrt((self.speed ** 2)/2) * level.dt
            self.rect.x += sqrt((self.speed ** 2)/2) * level.dt
        if self.now_direction == 2:
            self.rect.x += self.speed * level.dt
        if self.now_direction == 3:
            self.rect.y += sqrt((self.speed ** 2)/2) * level.dt
            self.rect.x += sqrt((self.speed ** 2)/2) * level.dt
        if self.now_direction == 4:
            self.rect.y += self.speed * level.dt
        if self.now_direction == 5:
            self.rect.y += sqrt((self.speed ** 2)/2) * level.dt
            self.rect.x -= sqrt((self.speed ** 2)/2) * level.dt
        if self.now_direction == 6:
            self.rect.x -= self.speed * level.dt
        if self.now_direction == 7:
            self.rect.y -= sqrt((self.speed ** 2)/2) * level.dt
            self.rect.x -= sqrt((self.speed ** 2)/2) * level.dt
