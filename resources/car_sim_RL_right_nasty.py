# -*- coding: utf-8 -*-

#-------------------
#实验强化学习主程序
#-------------------
from carClass import *
from numpy import *
#------------------------------------------------
#初始化，载入图片
#------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('车辆实验')
background = pygame.image.load('resources/image/map.png')
#定义各车道位置，偏移量，玩家速度，各车道速度
line_dist = 10
pos_list = [0+line_dist,60+line_dist,120+line_dist,180+line_dist,240+line_dist] #位置
player_speed = 300
speed_list = [200,160,100]
speed_list = [player_speed - speed_list[i] for i in range(len(speed_list))] #速度差列表
#车辆参数
plane_img = pygame.image.load('resources/image/carblack.png')
enemy1_rect = pygame.Rect(0, 0, 29, 45)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 0, 29, 45)))
enemies1 = pygame.sprite.Group()
# 玩家参数
plane_img = pygame.image.load('resources/image/car.png')
player_rect = pygame.Rect(0, 0, 29, 45)
player_pos = [120+ line_dist, 560]
player = Player(plane_img,player_rect, player_pos)



#------------------------------------------------
#状态集初始化
#------------------------------------------------

#五种行为模式的专家期望特征
#miu_e = array([ 0,  0.00799917,  0.29298774,  0.67201924,  0.02699385,  0])
#miu_e = array([ 0,  0,  0,  0.72639947,  0.27360053,  0])
miu_e = array([0.0, 0.0, 0.0, 0.27323533432740854, 0.54024167526954581, 0.18652299040304557])

last_miu = "empty"

#状态初始化
miu_export = [0,0,0,0,0,  0,0,0,0,0,0,0,0]#初始专家期望特征
w = [0.0,0,0,0,0,0]#初始权值
fi = [0,0,0,0,0     ,0,0,0,0,0,0,0,0]#初始特征向量
state = [8,8,8,8,8]

#主程序中用到的变量
clock = pygame.time.Clock()
car_time = 0 #出小车的时间间隔
miu_time = 0 #记录专家特征值的时间间隔
action_time = 0 #动作的延迟时间间隔
count_times = 0

#定义状态到特征的函数
def state_to_fi(s,i):
    fi = [0,0,0,0,0     ,0,0,0,0,0,0,0,0]
    current_dist = s[i]
    fi[i] = 1
    if current_dist != 8:
        fi[5+current_dist] = 1
    return fi

#------------------------------------------------
#主程序
#------------------------------------------------
Time = 100.0
w = [0,0,0,0,0,0]
#w= [-0.12980082490317893, -0.018521210209567606, -0.033810813572464127, -0.001537493378627075, 0.085508741868584537, 0.098161600195253093]
speed_list = list(array(speed_list)*1000.0/Time)
print "w=",
print w
player.rect[0] = pos_list[w.index(max(w[0:5]))]
while True:
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    car_time += time_passed
    miu_time += time_passed
    action_time += time_passed
    #----------------start paint-----------------#
    # 背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    # 绘制玩家汽车
    screen.blit(player.image, player.rect)
    # 随机生成汽车
    if car_time >=Time:
        for i in range(3):
            if len(enemies1)==0 or random.randint(0,50)>=(45-5*i):
                enemy1_pos = [pos_list[i+1], 0]
                enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos,speed_list[i])
                enemies1.add(enemy1)
        car_time = 0
    #移动敌机
    for enemy in enemies1:
        enemy.move(time_passed_seconds)
        if enemy.rect.top < 0:
            enemies1.remove(enemy)
    enemies1.draw(screen)
    # 更新屏幕
    pygame.display.update()
    #------------------end-------------------------#

    #----------------get state---------------------#
    #获取三个车道的状态
    state = [8,8,8,8,8]
    for enemy in enemies1:
        if (player.rect[1] - enemy.rect[1])<-60:
            continue
        idx_enemy = pos_list.index(enemy.rect[0])
        state[idx_enemy] = min([int(abs(player.rect[1]-enemy.rect[1])/80),state[idx_enemy]])
    #获取当前车道
    idx = pos_list.index(player.rect[0])
    fi = state_to_fi(state,idx)
    #------------------end--------------------------#

    #------- next state and reward -----------------#
    
    state_next = [8,8,8,8,8]
    for i in range(len(state)):
        state_next[i] = state[i] -1
        if state_next[i]==-1:
            state_next[i]=0
    #计算三种动作的奖励值
    (Rs,Rl,Rr) = (-100,-100,-100)
    fi_next = state_to_fi(state_next,idx)
    i=0
    Rs = sum([w[i]*fi_next[i] for i in range(len(w))])
    if idx>0:
        fi_next = state_to_fi(state_next,idx-1)
        Rl = sum([w[i]*fi_next[i] for i in range(len(w))])
    if idx<4:
        fi_next = state_to_fi(state_next,idx+1)
        Rr = sum([w[i]*fi_next[i] for i in range(len(w))])
    #-------------------end-------------------------#

    #-------------------action----------------------#
    if action_time>Time/10:
        R= [Rs,Rl,Rr]
        action = R.index(max(R));
        if action ==1:
            player.moveLeft()
        elif action ==2:
            player.moveRight()
        action_time = 0
    #-------------------end-------------------------#

    #------------------compute miu_export-----------#
    if miu_time>Time/10:
        miu_export = [miu_export[i]*0.99 +fi[i] for i in range(len(w))]
        count_times += 1
        miu_time = 0
    #---------------------end-----------------------#

    #----------------update w-----------------------#

    if count_times==1200:
        # now update miu_new
        sum_miu = sum(miu_export)
        miu = array(miu_export)/sum(miu_export)
        miu_export = [0,0,0,0,0,0]
        if sum((miu_e - miu)**2)<0.05:
            Time =1000
            count_times = 0
            print "w=",
            print w
        else:
            if last_miu =="empty":
                miu_new = miu
            else:
                miu_new = last_miu+ sum((miu-last_miu)*(miu_e-last_miu))/sum((miu-last_miu)*(miu-last_miu))*(miu-last_miu)
            w = list(miu_e - miu_new)
            last_miu = miu_new
            count_times = 0
            print "w=",
            print w
        
    #---------------------end ----------------------#

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
