import pygame
import tmx
import random

MAKEENEMY = pygame.USEREVENT+1
SWITCHLEVEL = pygame.USEREVENT+2
DEAD = pygame.USEREVENT+3

DEAD_EVENT = pygame.event.Event(DEAD)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, location, game, *groups):
        super(Enemy, self).__init__(*groups)
        self.enemy_dict = {}
        for en in [1, 2, 3, 4, 5, 9]:
            self.enemy_dict[en] = pygame.image.load('enemy' + str(en) + '.gif')
        self.image = self.enemy_dict[game.state]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.x_direction = random.uniform(-1, 1)
        self.y_direction = random.uniform(-1, 1)

    def update(self, game):

        #make enemies dance around the screen like poolballs

        self.rect.x += self.x_direction * 20 * game.dt * (game.state + 10)
        self.rect.y += self.y_direction * 20 * game.dt * (game.state + 10)
        if self.rect.x <= 0:
            self.x_direction = -self.x_direction
        if self.rect.x >= 770:
            self.x_direction = -self.x_direction
        if self.rect.y <= 0:
            self.y_direction = -self.y_direction
        if self.rect.y >= 420:
            self.y_direction = -self.y_direction

        if game.state != 5 and game.state != 9:
            if self.rect.colliderect(game.player.rect):
                pygame.event.post(DEAD_EVENT)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.sprite_dict = {}
        for animate in ['left', 'right', 'front', 'back']:
            self.sprite_dict[animate] = pygame.image.load("main_char_" + animate + ".png")
        self.image = self.sprite_dict['front']
        image_size = self.image.get_size()
        self.rect = pygame.rect.Rect((320, 370), (image_size[0] / 2, image_size[1] / 2))


    def update(self, game):

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 200 * game.dt
            self.image = self.sprite_dict['left']
        if key[pygame.K_RIGHT] and self.rect.x < 770:
            self.rect.x += 200 * game.dt
            self.image = self.sprite_dict['right']
        if key[pygame.K_UP] and self.rect.y > 350:
            self.rect.y -= 200 * game.dt
            self.image = self.sprite_dict['back']
        if key[pygame.K_DOWN] and self.rect.y < 420:
            self.rect.y += 200 * game.dt
            self.image = self.sprite_dict['front']


class Game(object):

    def __init__(self):
        self.state = 0 # game states allow us to progress through levels
        self.state_init = True
        self.start = pygame.time.get_ticks()
        self.victory = False

        self.demon_count = 0
        self.font = pygame.font.Font("calibri.ttf", 30)
        self.demonsurface = self.font.render("Demon Count is 0", False, (255,0,0))

        self.sprites = pygame.sprite.Group()
        self.player = Player(self.sprites)
        self.screen = pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(30) / 1000.0 # this is a measure in milliseconds
                                          # events are a function of gametime
        self.enemies = pygame.sprite.Group()
        pygame.time.set_timer(SWITCHLEVEL, 40000)
        self.is_dead = False


    def main(self):

        while True:
            self.view()
            self.timed_state_init()
            self.event_processor()

    def event_processor(self):

        for event in pygame.event.get():
            if event.type == MAKEENEMY:
                Enemy((random.randint(100, 700), random.randint(30, 300)), self, self.enemies)
                self.demon_count += 1
                self.demonsurface = self.font.render("Demon Count is {0}".format(self.demon_count),
                                                     False, (255,0,0))

            if event.type == SWITCHLEVEL:
                for enemy in self.enemies:
                    if isinstance(enemy, Enemy):
                        enemy.kill()
                self.state += 1
                self.state_init = True
                self.demon_count = 0
                if self.state != 9:
                    pygame.time.set_timer(MAKEENEMY, 3500 - (500 * self.state))
                self.start = pygame.time.get_ticks()
                self.load_music_background()
                if self.state == 5:
                    self.victory = True
                    pygame.time.set_timer(SWITCHLEVEL, 0)
                    self.player.kill()


            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()

            if event.type == DEAD:
                self.player.kill()
                for enemy in self.enemies:
                    if isinstance(enemy, Enemy):
                        enemy.kill()
                self.state = 9
                self.state_init = True
                self.start = pygame.time.get_ticks()
                self.load_music_background()
                pygame.time.set_timer(SWITCHLEVEL, 0)
                self.is_dead = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.is_dead == True or self.victory == True:
                    self.state = 0
                    self.state_init = True
                    self.victory = False
                    self.is_dead = False
                    self.demon_count = 0
                    pygame.time.set_timer(MAKEENEMY, 0)
                    pygame.time.set_timer(SWITCHLEVEL, 40000)
                    self.player = Player(self.sprites)

    def text_view(self, message):
        self.screen.fill((0, 0, 0))
        if self.state == 0:
            x = 135
        else:
            x = 290
        surface = self.font.render(message, False, (255,0,0))
        self.screen.blit(surface, (x, 225))
        pygame.display.flip()

    def timed_state_init(self):
        if pygame.time.get_ticks() > self.start + 3000:
           self.state_init = False
           if self.state == 0:
               event = pygame.event.Event(SWITCHLEVEL)
               pygame.event.post(event)

    def load_music_background(self):
        num = str(self.state)
        pygame.mixer.music.load('music' + num + '.ogg')
        pygame.mixer.music.play(-1)
        self.background = pygame.image.load('background' + num + '.jpeg')

    def view(self):

        if self.state_init == True:
            level_text = "LEVEL " + str(self.state) + " -- NOW DIE!!!"
            if self.state == 0:
                level_text = "WELCOME TO THE EVOLUTION OF EVIL!"
            if self.state == 5:
                level_text = " VICTORY! "
            if self.state == 9:
                level_text = " YOU DIED! "
            self.text_view(level_text)
            return

        if self.state_init == False:
            if self.state == 5 or self.state == 9:
                self.enemies.update(self)
                self.screen.blit(self.background, (0, 0))
                self.enemies.draw(self.screen)
                pygame.display.flip()
            else:
                self.sprites.update(self)
                self.enemies.update(self)
                self.screen.blit(self.background, (0, 0))
                self.sprites.draw(self.screen)
                self.enemies.draw(self.screen)
                self.screen.blit(self.demonsurface, (20, 20))
                pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    Game().main()