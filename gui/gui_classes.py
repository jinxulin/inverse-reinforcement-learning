import pygame
from numpy import array

SCREEN_WIDTH = 185
SCREEN_HEIGHT = 660
GUI_SPEED_MULTIPLE = 2
background = pygame.image.load('resources/image/map.png')


#create class Player
class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos, ini_speed):
        player_img = pygame.image.load('resources/image/car.png')
        player_rect = pygame.Rect(0, 0, 29, 45)
        self.image = player_img.subsurface(player_rect)
        self.rect = init_pos
        self.speed = ini_speed
        self.speed_horizontal = 60
        self.is_hit = False

    def speed_up(self):
        if self.speed < 150:
            self.speed += 30

    def slow_down(self):
        if self.speed > 30:
            self.speed -= 30

    def move_left(self):
        if self.rect[0] > self.speed_horizontal:
            self.rect[0] -= self.speed_horizontal

    def move_right(self):
        if self.rect[0] < SCREEN_WIDTH-self.speed_horizontal:
            self.rect[0] += self.speed_horizontal


#create class Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, init_pos, ini_speed):
        pygame.sprite.Sprite.__init__(self)
        enemy_img = pygame.image.load('resources/image/carblack.png')
        enemy_rect = pygame.Rect(0, 0, 29, 45)
        self.image = enemy_img.subsurface(enemy_rect)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = ini_speed
        self.down_index = 0
        self.pos = 0.0

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self, seconds):
        self.pos += self.speed * seconds * GUI_SPEED_MULTIPLE
        self.rect.top = self.pos












