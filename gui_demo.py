import random
from gui.gui_classes import *
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('car simulation')

# define the position of lane, bias, speed of player, speed of every lane
line_dist = 13
pos_list = array([0, 60, 120])+line_dist  # position
player_speed = 300
speed_list = array([200, 160, 100])
speed_list = player_speed - speed_list  # speed gap

# init player and enemies
player_pos = [120 + line_dist, 480]
player = Player(player_pos)
enemies = pygame.sprite.Group()

# other parameters
state = array([2, 8, 8, 8])
clock = pygame.time.Clock()
generate_time = 0  # time to build a new car
Time = 1000
key_push = False

while True:
    # calculate passed time
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    generate_time += time_passed

    # build the play's car and background
    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    # generate the car randomly
    if generate_time >= Time:
        for i in range(3):
            if len(enemies) == 0 or random.randint(0, 50) >= (45 - i*5):
                enemy_pos = [pos_list[i], 0]
                enemy = Enemy(enemy_pos, speed_list[i])
                enemies.add(enemy)
        generate_time = 0

    # move the enemy
    for enemy in enemies:
        enemy.set_speed(enemy.speed - player.speedGap)  # update the speed
        enemy.move(time_passed_seconds)
        if enemy.rect.top < 0:
            enemies.remove(enemy)
        enemy.set_speed(enemy.speed + player.speedGap)
    enemies.draw(screen)

    # update the screen
    pygame.display.update()

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

    # exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()