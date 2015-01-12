import sys
import numpy as np

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
        value_list = [np.dot(self.param, model._reward_function.features(s)) for s in state_list]
        action = value_list.index(max(value_list))
        return action
