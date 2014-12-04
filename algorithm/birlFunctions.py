from util.functions import *


#get probability for this index and action
def getActionProbability(valueDic, index, action, R):
    r = getIndexReward(index, R)
    idx1 = nextIndex(index, 0)
    idx2 = nextIndex(index, 1)
    idx3 = nextIndex(index, 2)
    v1 = valueDic[idx1]*0.9+r
    v2 = valueDic[idx2]*0.9+r
    v3 = valueDic[idx3]*0.9+r
    p = [math.exp(v1*0.5), math.exp(v2*0.5), math.exp(v3*0.5)]
    return p[action]/sum(p)


#get probability for the observed export list
def getObservedProbability(exportList, valueDic1, R1, valueDic2, R2):
    p = 1
    for item in exportList:
        index = item[0]
        action = item[1]
        pa = getActionProbability(valueDic2, index, action, R2) / getActionProbability(valueDic1, index, action, R1)
        p *= pa
    return p

'''
#get prior probability
def priorProbability(R):
    p=1
    x = [(abs(i)+0.02)**2 for i in R]
    for i in x:
        p *= 1/i
    return p
'''

def priorProbability(r1, r2):
    p = 1
    for i in range(len(r1)):
        pa = r2[i]**2 - r1[i]**2
        p *= 1/math.exp(pa*200)
    return p

#get birl probability P(R,policy)
def getBirlProbability(exportList, valueDic1, R1, valueDic2, R2):
    print R1
    print R2
    print "pr = " + str(priorProbability(R1, R2))
    p = getObservedProbability(exportList, valueDic1, R1, valueDic2, R2) * priorProbability(R1, R2)
    print "inner p = " + str(p)
    return p


#judge if current policy is optimal
def isOptimal(R, valueDic, policyDic):
    for index in valueDic:
        r = getIndexReward(index, R)
        qValue = valueDic[nextIndex(index, policyDic[index])]*0.9 + r
        idx1 = nextIndex(index, 0)
        idx2 = nextIndex(index, 1)
        idx3 = nextIndex(index, 2)
        v1 = valueDic[idx1]*0.9 + r
        v2 = valueDic[idx2]*0.9 + r
        v3 = valueDic[idx3]*0.9 + r
        if qValue < (max([v1, v2, v3])-0.00001):
            return False
    return True