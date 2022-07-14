import random
import numpy
import Gene

#TODO try to create a connection to action when a neutral is firstly created
class Individu:
    def __init__(self, connectionNumber, gridInfo, dadGenome = "", mutateChance= 0, score= 0):
        self.connectionNumber= connectionNumber
        self.score = score
        self.dadGenome = dadGenome
        self.genome = ""
        self.mutateChance = mutateChance
        self.params = gridInfo
        self.oldCoord = ()
        self.neutralDico = {}
        self.actionDico = {}
        if mutateChance == 0 and dadGenome != "":
            self.genome = dadGenome
        else:
            if dadGenome != "":
                self.createSonGene(self.dadGenome, self.mutateChance)
            else:
                #print("_-------_-------________________")
                self.createRandomGene(connectionNumber)
                #create random genome

    def randomSourceId(self):
        allSensor = Gene.getTypeGene("S")
        sourceType = str(random.randint(1, 6))
        if int(sourceType) > 1:
            sourceType = "0"
        if sourceType == "0":
            sourceId = allSensor[random.randint(0, len(allSensor) - 1)]
            neutralSource = ""
        else:
            neutralSource = str(bin(random.randint(100, 127)))[2:].zfill(7)
            sourceId = neutralSource
        return sourceId, neutralSource, sourceType

    def randomSinkId(self):
        allAction = Gene.getTypeGene("A")
        sinkType = str(random.randint(1, 6))
        if int(sinkType) > 1:
            sinkType = "0"
        if sinkType == "0":
            sinkId = allAction[random.randint(0, len(allAction) - 1)]
            neutral = ""
        else:
            neutral = str(bin(random.randint(100, 127)))[2:].zfill(7)

            sinkId = neutral
        return sinkId, neutral, sinkType
    #select random form sensor or internal then do connection to internal or action
    def createRandomGene(self, number):
        middleNodeUsed = []
        middleNodeConnected = False
        allNeutral = {}
        for _ in range(number):

            temp = self.randomSourceId()
            sourceId = temp[0]
            neutralSource = temp[1]
            sourceType = temp[2]

            temp = self.randomSinkId()
            sinkId = temp[0]
            neutralSink = temp[1]
            sinkType = temp[2]
            weight = str(bin(random.randint(0, 32767))).replace('0b', "").zfill(15)

            # 1 = negative
            weight = str(random.randint(0, 1)) + weight
            gene = sourceType + sourceId + sinkType + sinkId + weight
            gene = hex(int(gene, 2))[2:].zfill(8)
            if sourceType == "1" and sinkType == "0":
                if neutralSource in allNeutral.keys():
                    allNeutral[neutralSource] = [1, allNeutral[neutralSource][1] + " " +gene]
                else:
                    allNeutral[neutralSource] = [1, gene]
            elif sourceType == "1" and sinkType == "1":
                if neutralSource in allNeutral.keys():
                    allNeutral[neutralSource] = [2, allNeutral[neutralSource][1] + " " + gene, neutralSink]
                else:
                    allNeutral[neutralSource] = [2, gene, neutralSink]
            if sinkType=="1":
                if neutralSink not in allNeutral.keys():
                    allNeutral[neutralSink] = [0, gene]
                else:
                    allNeutral[neutralSink] = [0, allNeutral[neutralSink][1] + " " + gene]
            if self.genome != "":
                self.genome += " "
            self.genome += gene
        self.cleanUselessConnection(allNeutral)

    def createSonGene(self, dadGenome, mutateChance):
        newGenome = ""
        for value in dadGenome.split(" "):
            genome = bin(int(value, 16))[2:].zfill(32)
            inputType=genome[0]
            inputId=genome[1:8]
            sinkType=genome[8]
            sinkId=genome[9:16]
            weightNegative = genome[16]
            weight=genome[17:]
            #new random sensor
            if random.randint(0, 100) < mutateChance:
                temp = self.randomSourceId()
                inputType = temp[2]
                inputId = temp[0]
            if random.randint(0, 100) < mutateChance:
                temp = self.randomSinkId()
                sinkType = temp[2]
                sinkId = temp[0]
            if random.randint(0, 100) < mutateChance:
                weight = str(bin(random.randint(0, 32767))).replace('0b', "").zfill(15)
            if random.randint(0, 100) < mutateChance:
                weightNegative = str(random.randint(0, 1))
            gene = inputType + inputId + sinkType + sinkId + weightNegative + weight
            gene = hex(int(gene, 2))[2:].zfill(8)
            if newGenome != "":
                newGenome += " "
            newGenome += gene
        self.genome = newGenome

    def cleanUselessConnection(self, allNeutral):
        #si 2 fini dans 0 supprime 2
        for value in allNeutral:
            if allNeutral[value][0] == 0:
                for genome in allNeutral[value][1].split(" "):
                    if genome + " " in self.genome:
                        self.genome = self.genome.replace(genome + " ", "")
                    else:

                        self.genome = self.genome.replace(" " + genome, "")


    def move(self, newCoord):
        self.params[0] = newCoord

    def calculate(self, allCoord):
        params = [self.params[0], self.params[1], allCoord]
        # {"id": [[liste valeures], [cibles]]}
        self.oldCoord=self.params[0]
        allNeutral = {}
        allAction = {}
        #action: [[neutral, weight]]
        neutralToActionConnection = {}
        if self.genome == 0:
            return None
        for value in self.genome.split(" "):
            genome = bin(int(value, 16))[2:].zfill(32)
            inputType=genome[0]
            inputId=genome[1:8]
            sinkType=genome[8]
            sinkId=genome[9:16]
            weightNegative = genome[16]
            weight=genome[17:]
            weight = int(weight, 2) / 8191.75
            if weightNegative=="1":
                weight=-weight
            #call sensor then do math
            #sensor
            if inputType=="0":
                inputValue = Gene.callFunction(inputId, params)
                impulsion = inputValue*weight
                if sinkType == "0":
                    if sinkId not in allAction.keys():
                        allAction[sinkId] = [impulsion]
                    else:
                        allAction[sinkId].append(impulsion)
                else:
                    if sinkId not in allNeutral.keys():
                        allNeutral[sinkId] = [[impulsion], [], {}]
                    else:
                        allNeutral[sinkId][0].append(impulsion)
            #neutral
            elif inputType == "1":
                if inputId not in allNeutral.keys():
                    allNeutral[inputId] = [[0], [sinkId]]
                else:
                    allNeutral[inputId][1].append(sinkId)
                if sinkId not in neutralToActionConnection.keys():
                    neutralToActionConnection[sinkId] = [[], []]
                neutralToActionConnection[sinkId][0].append(inputId)
                neutralToActionConnection[sinkId][1].append(weight)
                if sinkType == "0":
                    if sinkId not in allAction.keys():
                        allAction[sinkId] = [0]
                else:
                    if sinkId not in allNeutral.keys():
                        allNeutral[sinkId] = [[0], []]
        #launch neutral to action
        for neutral in allNeutral.keys():
            sommeNeutral = numpy.tanh(sum(allNeutral[neutral][0]))
            for action in allNeutral[neutral][1]:
                if action in neutralToActionConnection:
                    if neutral in neutralToActionConnection[action][0]:
                        #get weight of neutral lol
                        impulsion = neutralToActionConnection[action][1][neutralToActionConnection[action][0].index(neutral)] * sommeNeutral

                else :
                    impulsion = sommeNeutral
                if action not in allAction:
                    allAction[action] = [impulsion]
                else:
                    allAction[action].append(impulsion)
        actionChoice = {}
        for action in allAction.keys():
            if action not in allNeutral:
                sommeAction = numpy.tanh(sum(allAction[action]))
                actionChoice[action] = sommeAction

        listOfKeys = [key for (key, value) in actionChoice.items() if value == max(actionChoice.values())]
        if len(listOfKeys) == 0:
            return None
        actionNeuronActivated = random.choice(listOfKeys)


        final = Gene.callFunction(actionNeuronActivated, params)
        if final == None:
            return "None"
        if final[0]>self.params[1] or final[0]<0:
            return "can't move"
        if final[1]>self.params[1] or final[1]<0:
            return "can't move"
        if final not in allCoord:
            self.move(final)


    #DONE: agissement de l'individu par rapoort a ces genes


#11110000111110100011101110011001
#_-------_-------________________