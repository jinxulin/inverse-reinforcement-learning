import os
import numpy as np


# read expert demo from file data/expert.txt
def read_expert_data(path):
    expert_data = []
    f = open(path)
    for line in f:
        fields = line.strip().split()
        state = [int(fields[i]) for i in range(len(fields))]
        expert_data.append(state)
    f.close()
    return expert_data


#compute_expert_feature
def compute_expect_feature(expert_data, reward_function):
    expert_feature = np.zeros(reward_function.dim)
    for line in expert_data:
        expert_feature += reward_function.features(np.array(line[0:-1]))
    return expert_feature/sum(expert_feature)
