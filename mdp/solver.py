import itertools
import math
import mdp.agent
import numpy as np
import random


class MDPSolver(object):
    def solve(self, model):
        raise NotImplementedError()


class QLearningSolver(MDPSolver):
    def __init__(self, max_iter):
        self.gamma = 0
        self.alpha = 0.1
        self._lambda = 0.5
        self.max_iter = max_iter
        self.z = np.zeros(11)

    def iterator(self, model, state, agent):
        fi = model._reward_function.features(state)
        v = np.dot(agent.param, fi)
        r = model.reward(state)
        if np.random.random() > 0.9:
            action = agent.take_action(model, state)
        else:
            action = random.sample(range(5), 1)[0]
        state_next = model.trans(state, action)
        fi_next = model._reward_function.features(state_next)
        v_next = np.dot(agent.param, fi_next)
        self.z = self.gamma * self._lambda * self.z + fi
        td = r + self.gamma * v_next - v
        agent.param += self.alpha * td * self.z
        return agent

    def solve(self, model):
        w = np.array([np.random.random()/100 for i in range(model.dim)])
        agent = mdp.agent.QValueAgent(w)
        for i in range(self.max_iter):
            agent = self.iterator(model, model.current_state(), agent)
        return agent





