from mdp.reward import LinearReward
import numpy as np


class DrivingReward(LinearReward):
    def __init__(self):
        super(LinearReward, self).__init__()

    def features(self, state, action=None):
        """features:
           0~2:lane   3~7:speed    8: is crashed
        """
        fi = np.zeros(11)
        lane = state[0]
        speed_level = state[4]/30
        distance = 480
        for i in range(3):
            if lane == i:
                distance = min(distance, abs(state[i+1]))
        fi[lane] += 1
        fi[speed_level+2] += 1
        if distance <= 120:
            fi[8 + distance/60] += 1
        return fi