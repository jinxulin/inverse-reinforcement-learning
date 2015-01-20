import sys
import numpy as np
import math


class Agent(object):
    """Representation of a policy"""

    """
    def sample(self, state):
        Returns a sample from actions(self,state)
        return sample(self.actions(state))
        """


class QValueAgent(Agent):
    """
        q value agent with function approximate
    """
    def __init__(self, param):
        self.param = param
        self.action_set = range(5)

    def take_action(self, model, state):
        state_list = [model.predict(state, a) for a in self.action_set]
        #print state_list
        #print self.param
        #print [model._reward_function.features(s) for s in state_list]
        value_list = [np.dot(self.param, model._reward_function.features(s)) for s in state_list]
        #print value_list
        action = value_list.index(max(value_list))
        return action

    def get_q_value(self, model, state, a):
        s = model.predict(state, a)
        q_value = np.dot(self.param, model._reward_function.features(s))
        return q_value

    def get_probability(self, model, state, a, alpha):
        state_list = [model.predict(state, a) for a in self.action_set]
        value_list = [np.dot(self.param, model._reward_function.features(s)) for s in state_list]
        p = [math.exp(v * alpha) for v in value_list]
        return p[a]/sum(p)