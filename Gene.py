import json
#50/100 - 0.5 =
#est border distance
import random


def EDB(params): #params = [coord, screenWeight, individuListe]
    return ((params[0][0]/params[1])-0.5)*2


#south border distance
def SBD(params):
    return ((params[0][1]/params[1])-0.5)*2


#detect somebody south
def DS(params):
    if (params[0][0], params[0][1]+10) in params[2]:
        return 1
    return 0


#detect somebody north
def DN(params):
    if (params[0][0], params[0][1] - 10) in params[2]:
        return 1
    return 0


#detect somebody west
def DW(params):
    if (params[0][0] - 10, params[0][1]) in params[2]:
        return 1
    return 0


#detect somebody est
def DE(params):
    if (params[0][0] + 10, params[0][1]) in params[2]:
        return 1
    return 0


#detect somebody south est
def DSW(params):
    if (params[0][0] - 10, params[0][1] + 10) in params[2]:
        return 1
    return 0


#detect somebody north est
def DSE(params):
    if (params[0][0] + 10, params[0][1] + 10) in params[2]:
        return 1
    return 0


#detect somebody south west
def DNW(params):
    if (params[0][0] - 10, params[0][1] - 10) in params[2]:
        return 1
    return 0


#detect somebody north west
def DNE(params):
    if (params[0][0] + 10, params[0][1] - 10) in params[2]:
        return 1
    return 0



#random input
def RNI(params):
    if random.randint(0, 1) == 1:
        return -random.random()
    else:
        return random.random()


#Move south
def MS(params):
    newCoord = (params[0][0], params[0][1] + 10)
    if newCoord < params[1]-10 and newCoord not in params[2]:
        return newCoord


#Move north
def MN(params):
    newCoord = (params[0][0], params[0][1] - 10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move west
def MW(params):
    newCoord = (params[0][0] - 10, params[0][1])
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move est
def ME(params):
    newCoord = (params[0][0] + 10, params[0][1])
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#moveRandom
def MR(params):
    newCoord = (params[0][0] + random.randint(-1,1), params[0][1] + random.randint(-1,1)*10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move south west
def MSW(params):
    newCoord = (params[0][0] - 10, params[0][1] + 10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move south est
def MSE(params):
    newCoord = (params[0][0] + 10, params[0][1] + 10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move north west
def MNW(params):
    newCoord = (params[0][0] - 10, params[0][1] +- 10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#Move north est
def MNE(params):
    newCoord = (params[0][0] + 10, params[0][1] - 10)
    if newCoord < params[1] - 10 and newCoord not in params[2]:
        return newCoord


#"0000111": [INTERNAL, "N"],
all_Gene={"0000000": [EDB, "S"],
            "0000001": [SBD, "S"],
            "0000010": [DS, "S"],
            "0000011": [DN, "S"],
            "0000100": [DW, "S"],
            "0000101": [DE, "S"],
            "0000110": [RNI, "S"],

            "0001000": [MS, "A"],
            "0001001": [MN, "A"],
            "0001010": [MW, "A"],
            "0001011": [ME, "A"],
            "0001100": [MR, "A"],
            "0001101": [MSW, "A"],
            "0001110": [MSE, "A"],
            "0001111": [MNW, "A"],
            "0010000": [MNE, "A"],
            "0010001": [DSW, "S"],
            "0010010": [DSE, "S"],
            "0010011": [DNW, "S"],
            "0010100": [DNE, "S"]
}
def getTypeGene(type):
    tab= []
    for key in all_Gene.keys():
        if all_Gene[key][1]==type:
            tab.append(key)
    return tab
def callFunction(name, params=None):
    if params is None:
        params = []
    return all_Gene[name][0](params)

