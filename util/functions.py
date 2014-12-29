#encoding:utf-8
import numpy as np
import random
import copy


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


#get action from two state
def get_action(s1, s2):
    lane1 = s1[0]
    lane2 = s2[0]
    speed1 = s1[4]
    speed2 = s1[4]
    if lane2 > lane1:
        return 1
    elif lane2 < lane1:
        return 2
    if speed1 > speed2:
        return 3
    elif speed1 < speed2:
        return 4
    return 0