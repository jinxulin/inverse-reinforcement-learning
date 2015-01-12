"""
create by Kintoki at 2014-12-30
"""

from mdp.reward import Reward


class State(object):
    pass


class Action(object):
    pass


class Model(object):
    """
    a mdp model
    """
    def __init__(self):
        self._gamma = 0.9
        self._reward_function = Reward()

    # executor the action
    def trans(self, state, action):
        """Returns a function state -> [0,1] for probability of next state
        given currently in state performing action"""
        raise NotImplementedError()

    # predict the next state, but not executor
    def predict(self, state, action):
        raise NotImplementedError()

    def reward(self, state, action=None):
        """Returns a reward for performing action in state"""
        return self.reward_function.get_reward(state, action)

    @property
    def gamma(self):
        """Discount factor over time"""
        return self._gamma

    @gamma.setter
    def gamma(self, gamma):
        self._gamma = gamma

    @property
    def reward_function(self):
        return self._reward_function

    @reward_function.setter
    def reward_function(self, rf):
        self._reward_function = rf