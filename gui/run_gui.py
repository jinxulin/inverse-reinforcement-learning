#encoding:utf-8

"""
run the experiment
input a agent
"""

from numpy import array
import random
from gui.gui_classes import *
from pygame.locals import *
from util.functions import *
import os


def run_gui(agent, model, Time=1000, write=False, write_path=""):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("car simulation: get expert's data")

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
    clock = pygame.time.Clock()
    generate_time = 0  # time to build a new car
    action_time = 0
    num_episode = 6
    num_write = 120
    record_time = 0  # time to write a record
    expert_records = []
    state = array([2, 480, 480, 480, player.speed])
    old_state = state
    fonts = pygame.font.get_fonts()
    my_font = pygame.font.SysFont("arial", 18)

    while True:
        # calculate passed time
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        generate_time += time_passed
        action_time += time_passed
        record_time += time_passed
        #print time_passed

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

        #get the state of three lane
        state = array([2, 480, 480, 480, player.speed])
        for enemy in enemies:
            if (player.rect[1] - enemy.rect[1]) <= -60:
                continue
            idx_enemy = list(pos_list).index(enemy.rect[0]) + 1
            state[idx_enemy] = min([int(abs(player.rect[1] - enemy.rect[1])), state[idx_enemy]])
        #get the current lane
        state[0] = list(pos_list).index(player.rect[0])

        #control by agent
        #print state
        #print model._reward_function.features(state)
        """
        if model._reward_function.features(state)[8] > 0:
            while True:
                print "is hit!!!!!!!!!!!!!!!!!!!!"
                break
            break
            """
        #print model._reward_function.params
        #print model.reward(state)
        #print agent.param

        if action_time > 0:
            action = agent.take_action(model, state)
            if action == 1:
                player.move_left()
            elif action == 2:
                player.move_right()
            elif action == 3:
                player.speed_up()
            elif action == 4:
                player.slow_down()
            #print "action=", action
            action_time = 0

        #write data to data.txt
        if record_time > Time/10:
            expert_records.append(list(old_state) + [get_action(old_state, state)])
            num_write -= 1
            old_state = state
            record_time = 0
        if num_write <= 0:
            if os.path.isfile("data/data.txt") and num_episode == 6:
                f = open("data/data.txt", "a")
            else:
                if not os.path.exists("data/"):
                    os.makedirs("data/")
                f = open("data/data.txt", "w")
            for line in expert_records:
                f.write('\t'.join([str(item) for item in line]) + "\n")
            f.close()
            num_write = 120
            num_episode -= 1
            print "written"

        if num_episode <= 0:
            break

        # update the screen
        pygame.display.update()

        # exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()