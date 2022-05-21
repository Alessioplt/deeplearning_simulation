import random
import numpy
import Gene


class Individu:
    def __init__(self, connectionNumber, gridInfo, dadGenome = ""):
        self.connectionNumber= connectionNumber

        self.dadGenome = dadGenome
        self.genome = ""
        self.params = gridInfo
        self.oldCoord = ()
        self.neutralDico = {}
        self.actionDico = {}
        if dadGenome != "":
            pass
            #create genome base on dad one
        else:
            #print("_-------_-------________________")
            self.createRandomGene(connectionNumber)
            #create random genome

    #select random form sensor or internal then do connection to internal or action
    def createRandomGene(self, number):
        middleNodeUsed = []
        middleNodeConnected = False
        allNeutral = {}
        for _ in range(number):
            allSensor = Gene.getTypeGene("S")
            allAction = Gene.getTypeGene("A")

            sourceType = str(random.randint(1, 6))
            if int(sourceType) > 1:
                sourceType  = "0"
            if sourceType == "0":
                sourceId = allSensor[random.randint(0, len(allSensor) - 1)]
            else:
                neutralSource = str(bin(random.randint(100,127)))[2:].zfill(7)
                sourceId = neutralSource

            sinkType = str(random.randint(1, 6))
            if int(sinkType) > 1:
                sinkType  = "0"
            if sinkType == "0":
                sinkId = allAction[random.randint(0, len(allAction) - 1)]
            else:
                neutral = str(bin(random.randint(100, 127)))[2:].zfill(7)

                sinkId = neutral

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
                    allNeutral[neutralSource] = [2, allNeutral[neutralSource][1] + " " + gene, neutral]
                else:
                    allNeutral[neutralSource] = [2, gene, neutral]
            if sinkType=="1":
                if neutral not in allNeutral.keys():
                    allNeutral[neutral] = [0, gene]
                else:
                    allNeutral[neutral] = [0, allNeutral[neutral][1] + " " + gene]
            if self.genome != "":
                self.genome += " "
            self.genome += gene
        self.cleanUselessConnection(allNeutral)



    def cleanUselessConnection(self, allNeutral):
        #si 2 fini dans 0 supprime 2
        for value in allNeutral:
            if allNeutral[value][0] == 0:
                for genome in allNeutral[value][1].split(" "):
                    if genome + " " in self.genome:
                        self.genome = self.genome.replace(genome + " ", "")
                    else:

                        self.genome = self.genome.replace(" " + genome, "")

            if allNeutral[value][0] == 2:
                if allNeutral[value][2] in allNeutral.keys():
                    if allNeutral[allNeutral[value][2]][0] == 0:
                        genome = allNeutral[value][1].split(" ")
                        for i in range(len(genome)):
                            if i != len(genome) - 1:
                                self.genome = self.genome.replace(genome[i] + " ", "")
                            else:
                                self.genome = self.genome.replace(" " + genome[i], "")


    def move(self, newCoord):
        self.params[0] = newCoord

    def calculate(self):
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
                inputValue = Gene.callFunction(inputId, self.params)
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
                    #neutralToActionConnection[sinkId] = []
                    allNeutral[inputId] = [[0], [sinkId]]
                else:
                    allNeutral[inputId][1].append(sinkId)²
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
                if action not in allAction:
                    allAction[action] = [sommeNeutral]
                else:
                    allAction[action].append(sommeNeutral)

        for action in allAction.keys():
            sommeAction = numpy.tanh(sum(allAction[action]))

        print(allNeutral)
        print(allAction)

    #TODO: agissement de l'individu par rapoort a ces genes


#11110000111110100011101110011001
#_-------_-------________________