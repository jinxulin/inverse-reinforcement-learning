#encoding:utf-8

"""
run the experiment environment
control the player's car by keyboard (up, down, speed_up, speed_down)
record state and export's action at that state
"""

from numpy import array
import random
import os
from gui.gui_classes import *
from pygame.locals import *
from util.functions import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("car simulation: get export's data")

# define the position of lane, bias, speed of player, speed of every lane
line_dist = 13
pos_list = line_dist + array([0, 60, 120])  # position
player_speed = 120
speed_list = array([90, 60, 30])

# init player and enemies
player_pos = [120 + line_dist, 480]
player = Player(player_pos, player_speed)
guidepost_list = [Guidepost((0, 0), player.speed), Guidepost((175, 0), player.speed)]
enemies = pygame.sprite.Group()

# other parameters
state = array([2, 480, 480, 480, player.speed/30])
old_state = state
export_records = []
num_write = 120
clock = pygame.time.Clock()
generate_time = 0  # time to build a new car
record_time = 0  # time to write a record
Time = 1000
key_push = False
fonts = pygame.font.get_fonts()
my_font = pygame.font.SysFont("arial", 18)

while True:
    # calculate passed time
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    generate_time += time_passed
    record_time += time_passed

    # build the player's car and background
    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    for guidepost in guidepost_list:
        screen.blit(guidepost.image, guidepost.rect)

    #show speed of player
    textSurfaceObj = my_font.render(str(player.speed)+"km/h", True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (92, 80)
    screen.blit(textSurfaceObj, textRectObj)

    # generate the car randomly
    if generate_time >= Time and len(enemies) < 7:
        for i in range(3):
            if len(enemies) == 0 or random.randint(0, 50) >= (45 - i * 5):
                enemy_pos = [pos_list[i], 0]
                enemy = Enemy(enemy_pos, speed_list[i], player.speed)
                enemies.add(enemy)
        generate_time = 0

    # move the guidepost
    for guidepost in guidepost_list:
        guidepost.set_environment_speed(player.speed)
        guidepost.move(time_passed_seconds)
        if guidepost.rect.top < 0 or guidepost.rect.top > 660:
            guidepost_list = [Guidepost((0, 0), player.speed), Guidepost((175, 0), player.speed)]
    # move the enemy
    for enemy in enemies:
        idx = list(pos_list).index(enemy.rect[0])
        enemy.set_environment_speed(player.speed)
        enemy.move(time_passed_seconds)
        if enemy.rect.top < 0 or enemy.rect.top > 660:
            enemies.remove(enemy)
    enemies.draw(screen)

    # update the screen
    pygame.display.update()

    #get the state of three lane
    state = array([2, 480, 480, 480, player.speed/30])
    for enemy in enemies:
        if (player.rect[1] - enemy.rect[1]) < -60:
            continue
        idx_enemy = list(pos_list).index(enemy.rect[0]) + 1
        state[idx_enemy] = min([int(abs(player.rect[1] - enemy.rect[1])), state[idx_enemy]])
    #get the current lane
    state[0] = list(pos_list).index(player.rect[0])
    new_state = state

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

    #write data to export.txt
    if record_time > Time/10:
        export_records.append(list(old_state) + [get_action(old_state, new_state)])
        num_write -= 1
        old_state = new_state
        record_time = 0

    if num_write <= 0:
        if os.path.isfile("data/export.txt"):
            f = open("data/export.txt", "a")
        else:
            f = open("data/export.txt", "w")
        for line in export_records:
            f.write('\t'.join([str(item) for item in line]) + "\n")
        f.close()
        num_write = 120
        print "written"

    # exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
