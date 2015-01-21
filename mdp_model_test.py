from driving.model import *
from driving.reward import DrivingReward
from mdp.solver import QLearningSolver
from numpy import array
from gui.run_gui import *

reward = DrivingReward()
reward.params = array([0.05, 0.02, 0.01, 0.2, 0.5, 0.6, 0.7, 0.8, -3, -0.05, -0.01])
#reward.params = array([0.15680481, 0.21396384, 0.00576546, 0.05409643, -0.01852762, 0.03494856,
#                       0.01832426, 0.14674493, -0.21742997, -0.04897249, 0.20452204])
model = DrivingModel()
model.reward_function = reward
model.dim = 11
qsolver = QLearningSolver(5000)
agent = qsolver.solve(model)
print agent.param
run_gui(agent, model)