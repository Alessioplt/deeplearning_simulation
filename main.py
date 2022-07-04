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
PINK = (255, 153, 204)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
generation = 1

def main(listePopulation, coordSafe, generation):
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    updateScreen(SCREEN, coordSafe, listePopulation)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #time.sleep(3)
        startSimutation(SCREEN, listePopulation, 150, 999999, coordSafe)
        #time.sleep(2)
        cleanBoard(SCREEN, listePopulation, coordSafe)
        print(f"Survived at gen {generation} = {len(listePopulation)}")
        # regenerateNewPopulation (ceux qui restent ce reproduisent)
        listePopulation = createNewGen(listePopulation, 1000, 10, WINDOW_HEIGHT)
        updateScreen(SCREEN, coordSafe, listePopulation)
        generation += 1
        graph = Graph(individuListe[0].genome, generation)
        graph.drawGraph()

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
    SCREEN.fill(PINK, coordSafe)
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

def createNewGen(listePopulation, number, numberGenome, taillegrille):
    listeCoord = []
    individusListe = []
    increment = 0
    for value in listePopulation:
        listeCoord.append(value.params[0])

    for _ in range(number):
        coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        while coord in listeCoord:
            coord = (random.randint(0, taillegrille / 10) * 10, random.randint(0, taillegrille / 10) * 10)
        listeCoord.append(coord)
        individusListe.append(Individu(numberGenome, [coord, taillegrille], listePopulation[increment].genome, 100))
        if increment==len(listePopulation)-1:
            increment=0
        else:
            increment+=1
    return individusListe

def getAllCoord(listePopulation):
    returnValue = {}
    for value in listePopulation:
        returnValue[value.genome] = value.params[0]
    return returnValue

def startSimutation(SCREEN, listePopulation, numberOfActionPerGen, actionPerSecond, coordSafe):

    for i in range(numberOfActionPerGen):
        allCoord = getAllCoord(listePopulation)
        for value in listePopulation:
            if ((value.params[0][0] >= coordSafe[0] and value.params[0][0] < coordSafe[2]) and (
                    value.params[0][1] >= coordSafe[1] and value.params[0][1] < coordSafe[3])):
                SCREEN.fill(PINK, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))

            else:
                SCREEN.fill(WHITE, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            value.calculate(allCoord.values())
            allCoord[value.genome] = value.params[0]
            if value == listePopulation[0]:
                SCREEN.fill(GREEN, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            else:
                SCREEN.fill(RED, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
        pygame.display.flip()
        time.sleep(1/actionPerSecond)

def cleanBoard(SCREEN, listePopulation, coordSafe):
    toRemove = []
    for value in listePopulation:
        if not(value.params[0][0] >= coordSafe[0] and value.params[0][0] < coordSafe[2]) or not(value.params[0][1] >= coordSafe[1] and value.params[0][1] < coordSafe[3]):
            SCREEN.fill(WHITE, (value.params[0][0] + 1, value.params[0][1] + 1, 8, 8))
            toRemove.append(value)
    for value in toRemove:
        listePopulation.remove(value)
    pygame.display.flip()

individuListe = createIndividus(1000, 10, WINDOW_HEIGHT)

graph = Graph(individuListe[0].genome, generation)
graph.drawGraph()
#taille de la grille en carré
grid = (0, 0, 10, 100)
main(individuListe, (grid[0], grid[1], grid[0]+grid[2]*10, grid[1]+grid[3]*10), generation)

#check les nouvelles position pour evité les collisions