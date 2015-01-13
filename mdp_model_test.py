from driving.model import *
from driving.reward import DrivingReward
from mdp.solver import QLearningSolver
import numpy as np
from gui.run_gui import *

reward = DrivingReward()
reward.params = np.array([0.5, 0.2, 0.1, 0, 0, 0.6, 0.8, 1, -3])
model = DrivingModel()
model.reward_function = reward
model.dim = 9
qsolver = QLearningSolver(10000)
agent = qsolver.solve(model)
print agent.param
run_gui(agent, model)
