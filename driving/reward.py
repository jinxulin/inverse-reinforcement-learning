from mdp.reward import LinearReward
import numpy as np


class DrivingReward(LinearReward):
    def __init__(self):
        super(LinearReward, self).__init__()

    def features(self, state, action=None):
        """features:
           0~2:lane   3~7:speed    8: is crashed
        """
        fi = np.zeros(9)
        lane = state[0]
        speed_level = state[4]/30
        is_crash = 0
        for i in range(3):
            if lane == i and abs(state[i+1]) < 60:
                is_crash = 1
        fi[lane] += 1
        fi[speed_level+2] += 1
        fi[-1] = is_crash
        return fi







