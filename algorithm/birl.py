from mdp.PolicyIterator import *
from algorithm.birlFunctions import *
from numpy import *
import copy


def birlSolver():

    #initialize
    stateList = initStateList()
    valueDic, policyDic = initDict(stateList)

    #get export data
    exportList = []
    exportData = open("data/export.txt")
    for line in exportData:
        record = line.strip().split()
        exportList.append([int(record[0]), int(record[1])])

    R = array([random.random()-0.5 for i in range(6)]) / 10
    valueDic, policyDic = solver(valueDic, policyDic, R)
    print "init done"
    loop = 0

    while True:
        loop += 1
        print "loop:"+str(loop)
        RNew = getReward(R)
        print RNew
        valueDicNew = valueEvaluation(valueDic, policyDic, RNew)

        if isOptimal(RNew, valueDicNew, policyDic):
            p = min([1, getBirlProbability(exportList, valueDic, R, valueDicNew, RNew)])
            print "p= " + str(p)
            if random.random() < p:
                R = RNew
                valueDic = copy.deepcopy(valueDicNew)
                print "reward update while policy do not update" + str(p)
            else:
                print "reward do not update 1: " + str(p)
        else:
            valueDicNew, policyDicNew = solver(valueDicNew, policyDic, RNew)
            p = min([1, getBirlProbability(exportList, valueDic, R, valueDicNew, RNew)])
            print "p= " + str(p)
            if random.random() < p:
                R = RNew
                policyDic = copy.deepcopy(policyDicNew)
                valueDic = copy.deepcopy(valueDicNew)
                print "reward and policy are updated" + str(p)
            else:
                print "reward do not update 2: " + str(p)

        rate = getProbability(exportList, policyDic)
        print "rate= " + str(rate)
        if rate > 0.802:
            break
    return R
