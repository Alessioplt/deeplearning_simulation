import time

import pygame
import sys
import random

from Graph import Graph
from Individu import Individu

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700


def main(listePopulation, checked):
    simulationStarted= False
    pygame.init()
    continueRunning = False
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)
    drawGrid(SCREEN)
    for value in listePopulation:
        if value == checked:
            SCREEN.fill(GREEN, (value.params[0][0]+1, value.params[0][1]+1, 8, 8))
            value.oldCoord = value.params[0]
        else:
            SCREEN.fill(RED, (value.params[0][0]+1, value.params[0][1]+1, 8, 8))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #update all genomes
                startSimutation(SCREEN, listePopulation, 60, 10)

        pygame.display.flip()


def drawGrid(screen):
    blockSize = 10  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)


def createIndividus(number, numberGenome, taillegrille, coordonneesInterdites = []):
    listeCoord = []
    individusListe = []

    for _ in range(number):
        coord = (random.randint(0,taillegrille/10)*10, random.randint(0,taillegrille/10)*10)
        while coord in listeCoord:
            coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        listeCoord.append(coord)
        individusListe.append(Individu(numberGenome, [coord, WINDOW_HEIGHT]))
    return individusListe

def startSimutation(SCREEN, listePopulation, numberOfActionPerGen, actionPerSecond):
    for i in range(numberOfActionPerGen):
        allCoord = getAllCoord(listePopulation)
        for value in listePopulation:
            SCREEN.fill(WHITE, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            value.calculate(allCoord)
            if value == listePopulation[0]:
                SCREEN.fill(GREEN, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            else:
                SCREEN.fill(RED, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
        pygame.display.flip()
        time.sleep(1/actionPerSecond)
def getAllCoord(listePopulation):
    returnValue = []
    for value in listePopulation:
        returnValue.append(value.params[0])
    return returnValue
individuListe = createIndividus(1000, 10, WINDOW_HEIGHT)

graph = Graph(individuListe[0].genome)
graph.drawGraph()
main(individuListe, individuListe[0])

#check les nouvelles position pour evité les collisions