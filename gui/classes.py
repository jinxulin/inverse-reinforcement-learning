#encoding:utf-8
#--------------------------
#define the classes
#--------------------------
import pygame
from numpy import *

SCREEN_WIDTH = 185
SCREEN_HEIGHT = 660

#import background image
background = pygame.image.load('resources/image/map.png')

#define the position of lane, bias, speed of player, speed of every lane
line_dist = 10
pos_list = array([0, 60, 120, 180, 240])+line_dist  # position
player_speed = 300
speed_list = array([200, 160, 100])
speed_list = player_speed - speed_list  # speed gap

# set parameter
plane_img = pygame.image.load('resources/image/carblack.png')
enemy1_rect = pygame.Rect(0, 0, 29, 45)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 0, 29, 45)))
enemies1 = pygame.sprite.Group()

# set player's parameter
plane_img = pygame.image.load('resources/image/car.png')
player_rect = pygame.Rect(0, 0, 29, 45)
player_pos = [120 + line_dist, 560]


#create class Player
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        self.image = plane_img.subsurface(player_rect)
        self.rect = init_pos
        self.speed = 60
        self.speedGap = 60
        self.is_hit= False
    def speedUp(self):
        if self.speedGap>0:
            self.speedGap -= 60
    def slowDown(self):
        if self.speedGap<180:
            self.speedGap += 60
    def moveLeft(self):
        if self.rect[0] > self.speed:
            self.rect[0] -= self.speed
    def moveRight(self):
        if self.rect[0] < SCREEN_WIDTH-self.speed:
            self.rect[0] += self.speed


#create class Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos,ini_speed):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       #self.rect.topleft = init_pos
       #self.down_imgs = enemy_down_imgs
       self.speed = ini_speed
       self.down_index = 0
       self.pos = 0.0
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
    def move(self, seconds):
        self.pos += self.speed*seconds
        self.rect.top = self.pos