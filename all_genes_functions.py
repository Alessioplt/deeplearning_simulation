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
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move north
def MN(params):
    newCoord = (params[0][0], params[0][1] - 10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move west
def MW(params):
    newCoord = (params[0][0] - 10, params[0][1])
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move est
def ME(params):
    newCoord = (params[0][0] + 10, params[0][1])
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#moveRandom
def MR(params):
    newCoord = (params[0][0] + random.randint(-1,1)*10, params[0][1] + random.randint(-1,1)*10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move south west
def MSW(params):
    newCoord = (params[0][0] - 10, params[0][1] + 10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move south est
def MSE(params):
    newCoord = (params[0][0] + 10, params[0][1] + 10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move north west
def MNW(params):
    newCoord = (params[0][0] - 10, params[0][1] - 10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord


#Move north est
def MNE(params):
    newCoord = (params[0][0] + 10, params[0][1] - 10)
    if newCoord[0] < params[1] - 1 and newCoord[1] < params[1] - 1 and newCoord not in params[2]:
        return newCoord

def DNO(params):
    return params[0]