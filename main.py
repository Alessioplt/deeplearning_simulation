import math
import time

import pygame
import sys
import random

from Graph import Graph
from Individu import Individu
from TimeSerieGenerator import TimeSeriegenerator
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 153, 204)
YELLOW = (255, 255, 0)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
generation = 1
numberConnection = 20
def main(listePopulation, coordSafe, generation, statsNuage):
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    updateScreen(SCREEN, coordSafe, listePopulation)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #time.sleep(3)
        #150 action
        startSimutation(SCREEN, listePopulation, 150, coordSafe)
        #time.sleep(2)
        cleanBoard(SCREEN, listePopulation, coordSafe)
        survivants = len(listePopulation)
        print(f"Survived at gen {generation} = {survivants}")
        # regenerateNewPopulation (ceux qui restent ce reproduisent)
        listePopulation = createNewGen(listePopulation, tailleSimulation, numberConnection, WINDOW_HEIGHT, generation)
        updateScreen(SCREEN, coordSafe, listePopulation)
        generation += 1
        statsNuage.addValue(generation-1, survivants)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()
        pygame.display.flip()


def drawGrid(screen):
    blockSize = 10  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)


def updateScreen(SCREEN, coordSafe, listePopulation):
    SCREEN.fill(WHITE)
    SCREEN.fill(PINK, (coordSafe[0], coordSafe[1], coordSafe[2]-coordSafe[0], coordSafe[3]-coordSafe[1]))
    coordX = ((coordSafe[2]-coordSafe[0])/2)+coordSafe[0]
    coordY = ((coordSafe[3]-coordSafe[1])/2)+coordSafe[1]
    SCREEN.fill(YELLOW, (coordX, coordY, 10, 10))
    drawGrid(SCREEN)

    for value in listePopulation:
        if value == listePopulation[0]:
            SCREEN.fill(GREEN, (value.params[0][0]+1, value.params[0][1]+1, 8, 8))
            value.oldCoord = value.params[0]
        else:
            SCREEN.fill(RED, (value.params[0][0]+1, value.params[0][1]+1, 8, 8))

def createIndividus(number, numberGenome, taillegrille, coordonneesInterdites = []):
    listeCoord = []
    individusListe = []

    for _ in range(number):
        coord = (random.randint(0,taillegrille/10)*10, random.randint(0,taillegrille/10)*10)
        while coord in listeCoord:
            coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        listeCoord.append(coord)
        individusListe.append(Individu(numberGenome, [coord, taillegrille]))
    return individusListe

def createNewGen(listePopulation, number, numberGenome, taillegrille, generation):
    listeCoord = []
    individusListe = []
    increment = 0
    listePopulation.sort(key=lambda x: x.score, reverse=True)
    Graph(listePopulation[0].genome, generation, listePopulation[0].score).drawGraph()
    numberReproductionLeft = listePopulation[increment].score // 10
    for value in listePopulation:
        listeCoord.append(value.params[0])

    while len(individusListe) < number:
        coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        while coord in listeCoord:
            coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        listeCoord.append(coord)
        if generation > 100:
            individusListe.append(Individu(numberGenome, [coord, taillegrille], listePopulation[increment].genome, mutateChance=0))
        else:
            individusListe.append(Individu(numberGenome, [coord, taillegrille], listePopulation[increment].genome, mutateChance=2))
        numberReproductionLeft -=1
        if numberReproductionLeft==0:
            if increment == len(listePopulation) - 1:
                increment = 0
            else:
                increment+=1
            numberReproductionLeft = listePopulation[increment].score // 10
    return individusListe

def getAllCoord(listePopulation):
    returnValue = {}
    for value in listePopulation:
        returnValue[value] = value.params[0]
    return returnValue


def startSimutation(SCREEN, listePopulation, numberOfActionPerGen, coordSafe):
    for i in range(numberOfActionPerGen):
        allCoord = getAllCoord(listePopulation)
        for value in listePopulation:
            if ((value.params[0][0] >= coordSafe[0] and value.params[0][0] < coordSafe[2]) and (
                    value.params[0][1] >= coordSafe[1] and value.params[0][1] < coordSafe[3])):
                SCREEN.fill(PINK, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))

            else:
                SCREEN.fill(WHITE, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            value.calculate(allCoord.values())
            allCoord[value] = value.params[0]
            if value == listePopulation[0]:
                SCREEN.fill(GREEN, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            else:
                SCREEN.fill(RED, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
        pygame.display.flip()

def cleanBoard(SCREEN, listePopulation, coordSafe):
    toRemove = []
    middleX = ((coordSafe[2]-coordSafe[0])/2)+coordSafe[0]
    middleY = ((coordSafe[3]-coordSafe[1])/2)+coordSafe[1]
    middleSafe = [middleX, middleY]
    distanceMiddleBorder = math.dist(middleSafe, [coordSafe[0], coordSafe[1]])
    for value in listePopulation:
        if not(value.params[0][0] >= coordSafe[0] and value.params[0][0] < coordSafe[2]) or not(value.params[0][1] >= coordSafe[1] and value.params[0][1] < coordSafe[3]):
            SCREEN.fill(WHITE, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            toRemove.append(value)
        else:
            dist = math.dist(middleSafe, value.params[0])
            value.score = int(100 - (dist*100/distanceMiddleBorder)) + 4
    for value in toRemove:
        listePopulation.remove(value)
    pygame.display.flip()


tailleSimulation = 1000
individuListe = createIndividus(tailleSimulation, numberConnection, WINDOW_HEIGHT)

statsNuage = TimeSeriegenerator(tailleSimulation)
#taille de la grille en carré

grid = (200, 200, 33, 33)
main(individuListe, (grid[0], grid[1], grid[0]+(grid[2]*10), grid[1]+(grid[3]*10)), generation, statsNuage)

#check les nouvelles position pour evité les collisions