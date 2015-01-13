from mdp.model import *
from driving.reward import DrivingReward
import numpy as np
import random
import copy

GUI_SPEED_MULTIPLE = 2
SPEED_LIST = [30, 60, 90]


class Car(object):
    def __init__(self, init_lane, init_pos, init_speed, init_environment_speed):
        self.pos = init_pos
        self.lane = init_lane
        self.speed = init_speed
        self.environment_speed = init_environment_speed

    def set_environment_speed(self, new_speed):
        self.environment_speed = new_speed

    def move(self, seconds):
        down_speed = self.environment_speed - self.speed
        self.pos += down_speed * seconds * GUI_SPEED_MULTIPLE


class MyCar(object):
    def __init__(self,  init_lane, init_pos,  init_speed):
        self.pos = init_pos
        self.speed = init_speed
        self.lane = init_lane

    def speed_up(self):
        if self.speed < 150:
            self.speed += 30

    def slow_down(self):
        if self.speed > 30:
            self.speed -= 30

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 2:
            self.lane += 1


class Environment(object):
    def __init__(self):
        self.player = MyCar(1, 480, 120)
        self.car_group = []
        self.speed_list = SPEED_LIST
        self.state = np.array([1, 480, 480, 480, self.player.speed])
        self.time_step = 0.1
        self.time_generate_car = 0
        self.gap_generate_car = 1

    def next_full_state(self):
        self.time_generate_car += 0.1
        if self.time_generate_car > self.gap_generate_car:
            self.time_generate_car = 0
            for i in range(3):
                if (len(self.car_group) == 0 or random.randint(0, 50) >= (45 - i * 5)) and len(self.car_group) < 7:
                    lane = i
                    pos = 0
                    car = Car(lane, pos, self.speed_list[i], self.player.speed)
                    self.car_group.append(car)
        for car in self.car_group:
            car.set_environment_speed(self.player.speed)
            car.move(self.time_step)
        self.car_group = [car for car in self.car_group if 0 < car.pos < 540]

    def get_state(self):
        state = [self.state[i] for i in range(len(self.state))]
        for car in self.car_group:
            idx = car.lane
            state[idx + 1] = min([int(self.player.pos - car.pos), self.state[idx + 1]])
        state[0] = self.player.lane
        state[4] = self.player.speed
        return state

    def action(self, a):
        if a == 1:
            self.player.move_left()
        elif a == 2:
            self.player.move_right()
        elif a == 3:
            self.player.speed_up()
        elif a == 4:
            self.player.slow_down()

    def show(self):
        print "cars:", len(self.car_group)
        print self.get_state()


class DrivingModel(Model):
    def __init__(self):
        super(Model, self).__init__()
        self.environment = Environment()
        self._reward_function = DrivingReward()
        self.dim = 9

    def trans(self, state, act):
        self.environment.action(act)
        self.environment.next_full_state()
        return self.environment.get_state()

    def predict(self, state_in, act):
        state = np.array(copy.copy(state_in))
        state[1:4] -= np.array(SPEED_LIST) * 0.2 * GUI_SPEED_MULTIPLE
        for i in range(len(state)):
            if state[i] < -60:
                state[i] = 480
        if act == 1 and state[0] > 0:
            state[0] -= 1
        elif act == 2 and state[0] < 2:
            state[0] += 1
        elif act == 3 and state[4] < 150:
            state[4] += 30
        elif act == 4 and state[4] > 30:
            state[4] -= 30
        return state

    def current_state(self):
        return self.environment.get_state()



