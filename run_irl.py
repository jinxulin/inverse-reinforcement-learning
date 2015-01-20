"""
Reference: 	Pieter Abbeel et al.  Apprenticeship learning via inverse reinforcement learning
create by Kintoki at 2014-12-25
"""
from driving.reward import *
from algorithm.irl_functions import *
from driving.model import *
from mdp.solver import *
from gui.run_gui import *
import copy

reward = DrivingReward()
reward.params = np.array([random.random()/10 for i in range(11)])
model = DrivingModel()
model.reward_function = reward
model.dim = 11
expert_data = read_expert_data("data/expert.txt")
miu_expert = compute_expect_feature(expert_data, reward)
qsolver = QLearningSolver(5000)

miu_bar_pre = np.zeros(model.dim)

while True:
    agent = qsolver.solve(model)
    run_gui(agent, model)
    run_data = read_expert_data("data/data.txt")
    miu_fi_expect = compute_expect_feature(run_data, reward)

    miu_bar = miu_bar_pre + \
        np.dot((miu_fi_expect - miu_bar_pre), (miu_expert - miu_bar_pre)) / \
        np.dot((miu_fi_expect - miu_bar_pre), (miu_fi_expect - miu_bar_pre)) \
        * (miu_fi_expect - miu_bar_pre)

    reward.params = miu_expert - miu_bar
    print agent.param
    print miu_bar_pre
    print miu_expert
    print miu_bar
    print reward.params
    t = (miu_expert - miu_fi_expect).std()
    miu_bar_pre = copy.deepcopy(miu_bar)

    """
        if t < 0.000001:
            print t
            break
    """