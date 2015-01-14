from driving.model import *
from driving.reward import DrivingReward
from mdp.solver import QLearningSolver
import numpy as np
from gui.run_gui import *

reward = DrivingReward()
reward.params = np.array([0.05, 0.02, 0.01, 0.2, 0.5, 0.6, 0.7, 0.8, -3, -0.05, -0.01])
model = DrivingModel()
model.reward_function = reward
model.dim = 11
qsolver = QLearningSolver(5000)
agent = qsolver.solve(model)
print agent.param
run_gui(agent, model)
