#encoding:utf-8
'''
sove the mdp by value iterator
'''
# solve mdp model
from util.functions import *
from numpy import *

#create state list
def initStateList():
	stateList = []
	for i in range(5):
		for j in range(9):
			for k in range(9):
				for l in range(9):
					stateList.append(stateToIndex([i,j,k,l]))
	return stateList

#create valueDic,transDic,policyDic
def initDict(stateList):
	valueDic = dict()
	transDic = dict()
	policyDic = dict()
	for index in stateList:
		valueDic[index] = 0
		transDic[index] = [stateToIndex(nextState(indexToState(index),0)),
				stateToIndex(nextState(indexToState(index),1)),
                stateToIndex(nextState(indexToState(index),2))]
	return valueDic,transDic,policyDic

#get value by index , valueDic and reward R
def getValue(index,valueDic,r):
    s0 = nextState(indexToState(index),0)
    s1 = nextState(indexToState(index),1)
    s2 = nextState(indexToState(index),2)
    v0 = valueDic[stateToIndex(s0)] *0.9
    v1 = valueDic[stateToIndex(s1)] *0.9
    v2 = valueDic[stateToIndex(s2)] *0.9
    r =  sum(computeFi(indexToState(index)) * r)
    V = array([v0,v1,v2]) + r
    return max(V)
	
#get policy dict
def getPolicy(valueDicIn):
    valueDic = valueDicIn
    policyDic =dict()
    for key in valueDic:
        idx0 = stateToIndex(nextState(indexToState(key),0))
        idx1 = stateToIndex(nextState(indexToState(key),1))
        idx2 = stateToIndex(nextState(indexToState(key),2))
        valueList = [valueDic[idx0],valueDic[idx1],valueDic[idx2]]
        policyDic[key] =  valueList.index(max(valueList))
    return policyDic

#value iterate
def solver(valueDicIn,R):
    valueDic  = valueDicIn
    i=0
    while True:
        i+=1
        final = True
        cost = 0
        for key in valueDic:
            newValue = getValue(key,valueDic,R)
            cost += abs( (valueDic[key] - newValue)**2 )
            valueDic[key] = newValue
        print i
        print cost
        if cost<0.005:
            break
    return valueDic

#get a new R base on this current reward R
def getReward(R):
    bias = array([(random.random()-0.5)/16 for i in range(6)])
    RNew = bias + array(R)
    for i in range(6): #R is never bigger than 1
        if abs(RNew[i])>1:
            RNew[i] = RNew[i]/abs(RNew[i])
    return RNew

#compute the probability of exportData  under R
def getProbability(exportList,PolicyDic):
    right = 0.0
    for record in exportList:
        if PolicyDic[record[0]] == record[1]:
            right += 1.0
    return right/len(exportList)

