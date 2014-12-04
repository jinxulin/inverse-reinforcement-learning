#encoding:utf-8
# solve mdp model
from util.functions import *
from numpy import *
import random
import os
import copy


#create state list
def initStateList():
    stateList = []
    for i in range(5):
        for j in range(9):
            for k in range(9):
                for l in range(9):
                    stateList.append(stateToIndex([i, j, k, l]))
    return stateList

#create valueDic,transDic,policyDic
def initDict(stateList):
    valueDic = dict()
    policyDic = dict()
    for index in stateList:
        valueDic[index] = 0
        policyDic[index] = random.randint(0, 2)
    return valueDic, policyDic

#get value by index , valueDic, policyDic and reward R
def getValue(index, valueDic, policyDic, r, gamma = 0.9):
    s = nextState(indexToState(index), policyDic[index])
    v = valueDic[stateToIndex(s)] * gamma
    reward = sum(computeFi(indexToState(index)) * r)
    return v+reward

#get policy dict
def getPolicy(valueDicIn):
    valueDic = valueDicIn
    policyDic =dict()
    for key in valueDic:
        idx0 = stateToIndex(nextState(indexToState(key), 0))
        idx1 = stateToIndex(nextState(indexToState(key), 1))
        idx2 = stateToIndex(nextState(indexToState(key), 2))
        valueList = [valueDic[idx0], valueDic[idx1], valueDic[idx2]]
        policyDic[key] = valueList.index(max(valueList))
    return policyDic


#value evaluation function
#def ...
def valueEvaluation(valueDicIn, policyDic, R, gamma = 0.9):
    valueDic = copy.deepcopy(valueDicIn)
    while True:
        cost = 0
        for index in valueDic:
            oldValue = valueDic[index]
            valueDic[index] = getValue(index, valueDic, policyDic, R, gamma)
            cost += abs(valueDic[index]-oldValue)
        print cost
        if cost < 0.005:
            break
    return valueDic

#policy iterate
def solver(valueDicIn, policyDicIn, R, gamma=0.9):
    valueDic = copy.deepcopy(valueDicIn)
    policyDic = copy.deepcopy(policyDicIn)
    for i in range(10):
        #value evaluation
        valueDic = valueEvaluation(valueDic, policyDic, R, gamma)
        #policy update
        policyDic = getPolicy(valueDic)
    return valueDic, policyDic

#get a new R base on this current reward R
def getReward(R):
    bias = array([(random.random()-0.5)/10 for i in range(6)])
    RNew = bias + array(R)
    for i in range(6): #R is never bigger than 1
        if abs(RNew[i]) > 1:
            RNew[i] = RNew[i]/abs(RNew[i])
    return RNew

#compute the probability of exportData  under R
def getProbability(exportList, PolicyDic):
    right = 0.0
    for record in exportList:
        if PolicyDic[record[0]] == record[1]:
            right += 1.0
    return right/len(exportList)
