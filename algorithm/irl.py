import numpy as np
from driving.reward import *
from irl_functions import *

reward = DrivingReward()
export_data = read_export_data("../data/export.txt")
print compute_export_feature(export_data, reward)