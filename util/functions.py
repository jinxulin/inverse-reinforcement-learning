#encoding:utf-8
from numpy import *
import random


#create the state list
def init_state_list(max_value_list):
    state_list = list()
    for i in range(max_value_list[0]):
        for j in range(max_value_list[1]):
            for k in range(max_value_list[2]):
                for l in range(max_value_list[3]):
                    for n in range(max_value_list[4]):
                        state_list.append(state_to_index([i, j, k, l, n]))
    return state_list


#create value dict
def init_value_dict(state_list):
    value_dict = dict()
    for index in state_list:
        value_dict[index] = 0
    return value_dict


#create policy dict
def init_policy_dict(state_list):
    policy_dict = dict()
    for index in state_list:
        policy_dict[index] = random.randint(0, 4)
    return policy_dict


#get the feather fi
def compute_fi(s):
    fi = [0, 0, 0, 0, 0, 0]
    fi[s[0]] += 1
    if s[0] < 4 and s[s[0]] <= 1:
        fi[5] += 1
    return array(fi)


#get next state
def next_state(state, a):
    s = state
    for i in range(3):
        if s[i+1] > 0:
            s[i+1] -= 1
    if s[0] != 0 and a == 1:
        s[0] -= 1
    elif s[0] != 4 and a == 2:
        s[0] += 1
    return s


#convert state to index
def index_to_state(idx):
    s = array([2, 8, 8, 8, 4])
    s[0] = int(idx / 10000)
    s[1] = int(idx % 10000 / 1000)
    s[2] = int(idx % 1000 / 100)
    s[3] = int(idx % 100 / 10)
    s[4] = int(idx % 10)
    return s


#convert index to state
def state_to_index(s):
    idx = s[0]*10000 + s[1]*1000 + s[2]*100 + s[3]*10 + s[4]
    return idx


#get action from two index
def get_action(index1, index2):
    s1 = int(index1 / 10000)
    s2 = int(index2 / 10000)
    speed1 = int(index1 % 10)
    speed2 = int(index2 % 10)
    if s2 > s1:
        return 1
    elif s2 < s1:
        return 2
    if speed1 > speed2:
        return 3
    elif speed1 < speed2:
        return 4
    return 0


#get next index
def next_index(index, a):
    state = index_to_state(index)
    state_next = next_state(state, a)
    return state_to_index(state_next)


#get index reward
def get_index_reward(index, R):
    state = compute_fi(index_to_state(index))
    return sum(state*R)