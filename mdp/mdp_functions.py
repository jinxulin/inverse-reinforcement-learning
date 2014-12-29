"""
the common functions to solver mdp
"""
import numpy as np


def compute_fi(state):
    fi = np.zeros(9)
    lane = state[0]
    speed_level = state[4] - 1
    fi[lane] += 1
    fi[speed_level + 3] += 1
    if abs(state[lane+1]) < 60:
        fi[-1] += 1
    return fi

