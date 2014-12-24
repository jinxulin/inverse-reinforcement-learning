#encoding:utf-8
from numpy import *


#get the feather fi
def computeFi(s):
    fi = [0,0,0,0,0,0]
    fi[s[0]]+=1
    if s[0]<4 and s[s[0]]<=1:
        fi[5]+=1
    return array(fi)


#get next state
def nextState(state,a):
    s = state
    for i in range(3):
        if s[i+1]>0:
            s[i+1]-=1
    if s[0]!=0 and a == 1:
        s[0]-=1
    elif s[0]!=4 and a == 2:
        s[0]+=1
    return s


#convert state to index
def indexToState(idx):
    s = array([2,8,8,8])
    s[0] = int(idx/1000)
    s[1] = int(idx%1000 /100)
    s[2] = int(idx%100 /10)
    s[3] = int(idx%10)
    return s


#convert index to state
def state_to_index(s):
    idx = s[0]*10000 + s[1]*1000 + s[2]*100 + s[3]*10 + s[4]
    return idx


#get action from two index
def get_action(index1, index2):
    s1 = int(index1 / 10000)
    s2 = int(index2 / 10000)
    speed1 = int(index1 % 10)
    speed2 = int(index2 % 10)

    if s2 > s1:
        return 1
    elif s2 < s1:
        return 2

    if speed1 > speed2:
        return 3
    elif speed1 < speed2:
        return 4

    return 0

#get next index
def nextIndex(index, a):
    state = indexToState(index)
    next_state = nextState(state, a)
    return stateToIndex(next_state)


#get index reward
def getIndexReward(index, R):
    state = computeFi(indexToState(index))
    return sum(state*R)