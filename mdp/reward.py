"""
create by Kintoki at 2014-12-30
"""
from numpy import dot


class Reward(object):
    """
    A Reward function stub
    """

    def __init__(self):
        self._params = []

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, _params):
        self._params = _params

    def get_reward(self, state, action):
        raise NotImplementedError()


class LinearReward(Reward):
    """
    A Linear Reward function stub

    params: weight vector equivalent to self.dim()
    """
    def features(self, state, action):
        raise NotImplementedError()

    @property
    def dim(self):
        raise NotImplementedError()

    def get_reward(self, state, action):
        print self.features(state, action)
        return dot(self._params, self.features(state, action))