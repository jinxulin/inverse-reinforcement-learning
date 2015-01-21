from algorithm.irl_functions import *
from driving.model import *
from mdp.solver import *
from numpy import array


# get a new reward base on this reward
def get_adjacent_reward(params):
    reward = copy.deepcopy(params)
    dim = len(reward)
    bias = (np.random.random(dim) - 0.5) / 10
    return reward + bias


# compute all q(s, a) for s, a in (S, A)
def compute_q_value(expert_data, agent, model):
    q_value_array = np.zeros(len(expert_data))
    for i in range(len(expert_data)):
        q_value_array[i] = agent.get_q_value(model, expert_data[i][0:-1], expert_data[i][-1])
    return q_value_array


# compute the
def compute_probability(expert_data, agent, new_agent, model):
    p = 1
    for i in range(len(expert_data)):
        state = expert_data[i][0:-1]
        action = expert_data[i][-1]
        p1 = agent.get_probability(model, state, action, 0.5)
        p2 = new_agent.get_probability(model, state, action, 0.5)
        p *= p2 / p1
    return p


# the reward's prior
def prior_probability(r1, r2):
    p = 1
    for i in range(len(r1)):
        pa = r2[i]**2 - r1[i]**2
        p *= 1/math.exp(pa*200)
    return p


# compute rate of right action
def get_rate(expert_data, model, agent):
    same_action = 0.0
    for i in range(len(expert_data)):
        if expert_data[i][-1] == agent.take_action(model, expert_data[i][0:-1]):
            same_action += 1.0
    return same_action/len(expert_data)


# bayesian inverse reinforcement learning algorithm
# 1. set the model and pick a random reward vector R
reward = DrivingReward()
reward.params = np.array([random.random()/10 for i in range(11)])
model = DrivingModel()
model.reward_function = reward
model.dim = 11
expert_data = read_expert_data("data/expert.txt")

# 2. solve the model , using q learning solver
qsolver = QLearningSolver(5000)
agent = qsolver.solve(model)

# 3. repeat to update the reward r
while True:
    # a. pick a random r~ from the neighbours of r
    old_reward_params = copy.copy(reward.params)
    new_reward_params = get_adjacent_reward(reward.params)
    print "reward = ", new_reward_params
    reward.params = copy.copy(new_reward_params)
    # b. compute all q(s, a, r~) for all s, a
    #q_value_array = array([agent.get_q_value(model, state[0:-1], state[-1]) for state in expert_data])
    # c. get new agent. update r
    if True:  # this line need to be fixed
        new_agent = qsolver.solve(model)
        """
        p = compute_probability(expert_data, agent, new_agent, model) * prior_probability(old_reward_params, new_reward_params)
        print p
        print reward.params
        """
        rate1 = get_rate(expert_data, model, agent)
        print "rate1=", rate1
        rate2 = get_rate(expert_data, model, new_agent)
        print "rate2=", rate2

        if rate2 > rate1:
            reward.params = copy.copy(new_reward_params)
            agent = new_agent
        else:
            reward.params = copy.copy(old_reward_params)

        if rate1 > 0.8:
            break