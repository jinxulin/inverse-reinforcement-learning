#encoding:utf-8

"""
run the experiment environment
control the player's car by keyboard (up, down, speed_up, speed_down)
record state and export's action at that state
"""

import random
from numpy import array
from gui.gui_classes import *
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("car simulation: get export's data")

# define the position of lane, bias, speed of player, speed of every lane
line_dist = 13
pos_list = line_dist + array([0, 60, 120])  # position
player_speed = 120
speed_list = array([90, 60, 30])
speed_list = player_speed - speed_list  # speed gap

# init player and enemies
player_pos = [120 + line_dist, 480]
player = Player(player_pos, player_speed)
enemies = pygame.sprite.Group()

# other parameters
state = array([2, 8, 8, 8, player.speed])
clock = pygame.time.Clock()
generate_time = 0  # time to build a new car
Time = 1000
key_push = False

while True:
    # calculate passed time
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    generate_time += time_passed

    # build the player's car and background
    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    # generate the car randomly
    if generate_time >= Time:
        for i in range(3):
            if len(enemies) == 0 or random.randint(0, 50) >= (45 - i * 5):
                enemy_pos = [pos_list[i], 0]
                enemy = Enemy(enemy_pos, speed_list[i])
                enemies.add(enemy)
        generate_time = 0

    # move the enemy
    for enemy in enemies:
        #enemy.set_speed(enemy.speed - player.speed)  # update the speed
        enemy.move(time_passed_seconds)
        if enemy.rect.top < 0:
            enemies.remove(enemy)
        #enemy.set_speed(enemy.speed + player.speed)
    enemies.draw(screen)

    # update the screen
    pygame.display.update()

    #get the state of three lane
    state = array([2, 8, 8, 8, player.speed/30])
    for enemy in enemies:
        if (player.rect[1] - enemy.rect[1]) < -60:
            continue
        idx_enemy = list(pos_list).index(enemy.rect[0]) + 1
        state[idx_enemy] = min([int(abs(player.rect[1] - enemy.rect[1])/60), state[idx_enemy]])
    #get the current lane
    state[0] = list(pos_list).index(player.rect[0])
    print state

    #keybroad control
    if not key_push:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            player.move_left()
            key_push = True
        elif pressed_keys[K_RIGHT]:
            player.move_right()
            key_push = True
        elif pressed_keys[K_UP]:
            player.speed_up()
            key_push = True
        elif pressed_keys[K_DOWN]:
            player.slow_down()
            key_push = True
    if key_push:
        pressed_keys = pygame.key.get_pressed()
        if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]):
            key_push = False

    '''
    #------------------record-----------------------#
    if newStateIndex != oldStateIndex:
        exportRecords.append([oldStateIndex, getAction( newStateIndex, oldStateIndex)])
        oldStateIndex = newStateIndex
        writeNum -= 1
    if writeNum<=0:
        f = open("data/export.txt","a")
        for line in exportRecords:
            f.write(str(line[0])+"\t"+str(line[1])+"\n")
        f.close()
        writeNum=120
        print "written"
    '''

    # exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
