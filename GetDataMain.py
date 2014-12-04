# -*- coding: utf-8 -*-

#-------------------
#record the export's demo
#-------------------
from numpy import *
from util.functions import *
from util.classes import *
#------------------------------------------------
#initialize and load picture
#------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('car simulation')
background = pygame.image.load('resources/image/map.png')
#define the position of lane, bias, speed of player, speed of every lane
line_dist = 10
pos_list = array([0, 60, 120, 180, 240])+line_dist #position
player_speed = 300
speed_list = array([200, 160, 100])
speed_list = player_speed - speed_list #speed gap
#set parameter
plane_img = pygame.image.load('resources/image/carblack.png')
enemy1_rect = pygame.Rect(0, 0, 29, 45)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 0, 29, 45)))
enemies1 = pygame.sprite.Group()
# set player's parameter
plane_img = pygame.image.load('resources/image/car.png')
player_rect = pygame.Rect(0, 0, 29, 45)
player_pos = [120+ line_dist, 560]
player = Player(plane_img, player_rect, player_pos)


#------------------------------------------------
#initialize
#------------------------------------------------

state = array([2,8,8,8])

#define variable
clock = pygame.time.Clock()
car_time = 0 #time to build a new car
action_time = 0 #delay time of action
Time = 1000
key_push = False
exportRecords = []
oldStateIndex = stateToIndex(state)
writeNum = 120

#------------------------------------------------
#main 
#------------------------------------------------
while True:
    time_passed = clock.tick()
    #print time_passed
    time_passed_seconds = time_passed / 1000.0
    car_time += time_passed
    action_time += time_passed

    #----------------start paint-----------------#
    # background
    screen.fill(0)
    screen.blit(background, (0, 0))
    # build the play's car
    screen.blit(player.image, player.rect)
    # generate the car randomly
    if car_time >=Time:
        for i in range(3):
            if len(enemies1)==0 or random.randint(0,50)>= (45 - i*5):
                enemy1_pos = [pos_list[i+1], 0]
                enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos,speed_list[i])
                enemies1.add(enemy1)
        car_time = 0
    # move the enemy
    for enemy in enemies1:
        enemy.move(time_passed_seconds)
        if enemy.rect.top < 0:
            enemies1.remove(enemy)
    enemies1.draw(screen)
    # update the screen
    pygame.display.update()
    #------------------end-------------------------#

    #----------------get state---------------------#
    #get the state of three lane
    state = array([2,8,8,8])
    for enemy in enemies1:
        if (player.rect[1] - enemy.rect[1])<-60:
            continue
        idx_enemy = list(pos_list).index(enemy.rect[0])
        state[idx_enemy] = min([int(abs(player.rect[1]-enemy.rect[1])/80),state[idx_enemy]])
    #get the current lane
    state[0] = list(pos_list).index(player.rect[0])
    newStateIndex = stateToIndex(state)
    #------------------end--------------------------#

    #-------------------action----------------------#
    #keybroad control
    if key_push == False:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            player.moveLeft()
            action = 1;
            key_push = True
        elif pressed_keys[K_RIGHT]:
            player.moveRight()
            key_push = True
    if key_push:
        pressed_keys = pygame.key.get_pressed()
        if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]):
            key_push = False
    #-------------------end-------------------------#

    #------------------record-----------------------#
    if newStateIndex!= oldStateIndex:
        exportRecords.append([oldStateIndex,getAction( newStateIndex, oldStateIndex)])
        oldStateIndex = newStateIndex
        writeNum -= 1
    if writeNum<=0:
        f = open("data/export.txt","a")
        for line in exportRecords:
            f.write(str(line[0])+"\t"+str(line[1])+"\n")
        f.close()
        writeNum=120
        print "written"
    # exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

