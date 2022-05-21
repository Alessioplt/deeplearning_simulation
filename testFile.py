import random
import Gene
from Graph import Graph


class Individu:
    def __init__(self, connectionNumber, gridInfo, dadGenome = ""):
        self.connectionNumber= connectionNumber

        self.dadGenome = dadGenome
        self.genome = ""
        self.params = gridInfo

        self.neutralDico = {}
        self.actionDico = {}
        if dadGenome != "":
            pass
            #create genome base on dad one
        else:
            #print("_-------_-------________________")
            pass
            #self.createRandomGene(connectionNumber)
            #create random genome

    #select random form sensor or internal then do connection to internal or action
    def createRandomGene(self, number):
        middleNodeUsed = []
        middleNodeConnected = False
        allNeutral = {}
        for _ in range(number):
            allSensor = Gene.getTypeGene("S")
            allAction = Gene.getTypeGene("A")

            sourceType = str(random.randint(0, 1))
            if sourceType == "0":
                sourceId = allSensor[random.randint(0, len(allSensor) - 1)]
            else:
                neutralSource = str(bin(random.randint(100,127)))[2:].zfill(7)
                sourceId = neutralSource

            sinkType = str(random.randint(0, 1))
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
        print(allNeutral)
        print(self.genome)
        #si 2 fini dans 0 supprime 2
        for value in allNeutral:
            if allNeutral[value][0] == 0:
                for genome in allNeutral[value][1].split(" "):
                    if genome+" " in self.genome:
                        print(self.genome)
                        self.genome = self.genome.replace(genome + " ", "")
                        print(self.genome)
                    else:

                        self.genome = self.genome.replace(" " + genome, "")

            elif allNeutral[value][0] == 2:
                if allNeutral[value][2] in allNeutral.keys():
                    if allNeutral[allNeutral[value][2]][0] == 0:
                        genome = allNeutral[value][1].split(" ")
                        for i in range(len(genome)):
                            if i != len(genome) - 1:
                                self.genome = self.genome.replace(genome[i] + " ", "")
                            else:
                                self.genome = self.genome.replace(" " + genome[i], "")
                            print(self.genome)



    def move(self, newCoord):
        self.params[0] = newCoord

    def calculate(self):
        #{"id": }
        allNeutral = {}
        if self.genome == 0:
            print("test")
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
            #call sensor then do math
            inputValue = Gene.callFunction(inputId, self.params)
            print(weight)

        #TODO faire  la verif de connection qui aboutisses jamais
    #TODO: agissement de l'individu par rapoort a ces genes


#00010010111011101011001100011000
#_-------_-------________________

gene = Individu(10, [])
gene.genome= "f6e847d0 060cccad 05089591 050c9be8 02e6becf fdf7d5d0 000f2df7 f00ec3d3 030a52a2 12eeb318"
gene.cleanUselessConnection(
{'1110110': [2, 'f6e847d0', '1101000'], '1101000': [0, 'f6e847d0'], '1100110': [0, '02e6becf'], '1111101': [2, 'fdf7d5d0', '1110111'], '1110111': [0, 'fdf7d5d0'], '1110000': [1, 'f00ec3d3'], '1101110': [0, '12eeb318']}
)
graph = Graph(gene.genome)
graph.drawGraph()