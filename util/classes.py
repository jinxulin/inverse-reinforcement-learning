#encoding:utf-8
#--------------------------
#define the classes
#--------------------------
import pygame
from sys import exit
from pygame.locals import *
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 800

#import background image
background = pygame.image.load('resources/image/map.png')

#create class Player
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        self.image = plane_img.subsurface(player_rect)
        self.rect = init_pos
        self.speed = 60
        self.is_hit= False
        
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
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = ini_speed
       self.down_index = 0
       self.pos = 0.0
    def move(self,seconds):
        self.pos += self.speed*seconds
        self.rect.top = self.pos
