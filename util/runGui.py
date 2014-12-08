from numpy import *
from util.functions import *
from util.classes import *
from mdp.PolicyIterator import *
#-------------------
# main
#-------------------


def run_gui(w):
    #------------------------------------------------
    #initialize and load picture
    #------------------------------------------------

    #initialize
    stateList = initStateList()
    print stateList
    valueDic, policyDic = initDict(stateList)
    valueDic, policyDic = solver(valueDic, policyDic, w, 0)

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('car simulation')
    background = pygame.image.load('resources/image/map.png')
    #define the position of lane, bias, speed of player, speed of every lane
    line_dist = 10
    pos_list = [0+line_dist, 60+line_dist, 120+line_dist, 180+line_dist, 240+line_dist] #position
    player_speed = 300
    speed_list = [200, 160, 100]
    speed_list = [player_speed - speed_list[i] for i in range(len(speed_list))] #speed gap
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
    player_pos = [120 + line_dist, 560]
    player = Player(plane_img,player_rect, player_pos)


    #------------------------------------------------
    #initialize
    #------------------------------------------------

    clock = pygame.time.Clock()
    car_time = 0 
    miu_time = 0 
    action_time = 0
    Time = 1000


    speed_list = list(array(speed_list)*1000/Time)
    print "w=",
    print w
    while True:
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        car_time += time_passed
        miu_time += time_passed
        action_time += time_passed
        #----------------start paint-----------------#
        screen.fill(0)
        screen.blit(background, (0, 0)) 
        screen.blit(player.image, player.rect)
        if car_time >= Time:
            for i in range(3):
                if len(enemies1) == 0 or random.randint(0, 50)>=(45-5*i):
                    enemy1_pos = [pos_list[i+1], 0]
                    enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos, speed_list[i])
                    enemies1.add(enemy1)
            car_time = 0
        for enemy in enemies1:
            enemy.move(time_passed_seconds)
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
        enemies1.draw(screen)
        pygame.display.update()
        #------------------end-------------------------#

        #----------------get state---------------------#
        state = [8,8,8,8,8]
        for enemy in enemies1:
            if (player.rect[1] - enemy.rect[1])<-60:
                continue
            idx_enemy = pos_list.index(enemy.rect[0])
            state[idx_enemy] = min([int(abs(player.rect[1]-enemy.rect[1])/80), state[idx_enemy]])
        idx = pos_list.index(player.rect[0])

        mystate = idx*1000 + state[1]*100 + state[2]*10 + state[3]
        #------------------end--------------------------#

        #-------------------action----------------------#
        if action_time > Time/10:
            try:
                action = policyDic[mystate]
                if action == 1:
                    player.moveLeft()
                elif action == 2:
                    player.moveRight()
                action_time = 0
            except:
                pass
        #-------------------end-------------------------#
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
