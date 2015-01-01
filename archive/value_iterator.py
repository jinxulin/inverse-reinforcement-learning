from util.functions import *


def get_value(index, value_dict, R, gamma):
    s = range(5)
    v = range(5)
    for i in range(5):
        s[i] = next_state(index_to_state(index), i)
    for i in range(5):
        v[i] = value_dict[s[i]] * gamma
    r = sum(compute_fi(index_to_state(index)) * R)
    return max(v) + r


def value_iterator_solver(R):
    state_list = init_state_list([5, 9, 9, 9, 9])
    value_dict = init_value_dict(state_list)
    while True:
        cost = 10000
        for key in value_dict:
            new_value = get_value(key, value_dict, R, gamma=0.9)
            cost = min((value_dict[key] - new_value)**2, cost)
            value_dict[key] = new_value
        print cost
        if cost < 0.005:
            break
    return value_dict


def get_policy(value_dict):
    policy_dict = dict()
    idx = range(5)
    v = range(5)
    for index in value_dict:
        for i in range(5):
            idx[i] = next_state(index_to_state(index), i)
        for i in range(5):
            v[i] = value_dict[idx[i]]
        policy_dict[index] = v.index(max(v))
    return policy_dict