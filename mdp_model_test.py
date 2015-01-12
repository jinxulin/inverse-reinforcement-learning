from driving.model import *
from driving.reward import DrivingReward
from mdp.solver import QLearningSolver
import numpy as np
"""
car_groups = []
for i in range(100):
    car = Car(1, 20, 40, 50)
    car_groups.append(car)
    print len(car_groups)

car_groups = [car for car in car_groups if car.pos < 540 or car.pos > 0]
print len(car_groups)
"""

reward = DrivingReward()
reward.params = np.array([0.1, 0, 0, 0, 0, 0, 0, 1, -2])
model = DrivingModel()
model.reward_function = reward
model.dim = 9
qsolver = QLearningSolver(1000)

agent = qsolver.solve(model)