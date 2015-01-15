import os
import numpy as np


# read export demo from file data/export.txt
def read_export_data(path):
    export_data = []
    f = open(path)
    for line in f:
        fields = line.strip().split()
        state = [int(fields[i]) for i in range(len(fields))]
        export_data.append(state)
    f.close()
    return export_data


#compute_export_feature
def compute_export_feature(export_data, reward_function):
    export_feature = np.zeros(reward_function.dim)
    for line in export_data:
        export_feature += reward_function.features(np.array(line[0:-1]))
    return export_feature/len(export_data)
