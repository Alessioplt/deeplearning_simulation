import glob
import os

import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
from datetime import date

import json
class Graph:
    def __init__(self, genome, generation, score):
        self.score = score
        self.genome = genome
        self.generation = generation
        self.genesList =json.load(open('genes.json'))
        self.pos = {}
        self.listeSensor = []
        self.listeNeutral = []
        self.listeAction = []

    def drawGraph(self, today=None, run=None):
        G = nx.Graph()
        #1,7,1,7,16
        for value in self.genome.split(" "):
            genome = bin(int(value, 16))[2:].zfill(32)
            inputType=genome[0]
            inputId=genome[1:8]
            sinkType=genome[8]
            sinkId=genome[9:16]
            weightNegative = genome[16]
            weight=genome[17:]
            if inputType=="0":
                self.listeSensor.append(inputId) if inputId not in self.listeSensor else self.listeSensor
            else:
                self.listeNeutral.append(inputId) if inputId not in self.listeNeutral else self.listeNeutral
            if sinkType=="0":
                self.listeAction.append(sinkId) if sinkId not in self.listeAction else self.listeAction
            else:
                self.listeNeutral.append(sinkId) if sinkId not in self.listeNeutral else self.listeNeutral
            weight = int(weight, 2)/8191.75

            if weightNegative=="1":
                weight=-weight
            if inputType == "1":
                if sinkType == "1":
                    G.add_edge(inputId, sinkId, weight=weight)
                else:
                    G.add_edge(inputId, self.genesList[sinkId], weight=weight)
            elif sinkType == "1":
                G.add_edge(self.genesList[inputId], sinkId, weight=weight)
            else:
                G.add_edge(self.genesList[inputId], self.genesList[sinkId], weight=weight)
        middle = (max([len(self.listeSensor), len(self.listeNeutral), len(self.listeAction)])-1)/2
        for i in range (len(self.listeSensor)):
            self.pos[self.genesList[self.listeSensor[i]]] = (i,1)
        for i in range (len(self.listeNeutral)):
            self.pos[self.listeNeutral[i]] = (i,0)
        for i in range (len(self.listeAction)):
            self.pos[self.genesList[self.listeAction[i]]] = (i,-1)


        nx.draw_networkx_nodes(G, self.pos, node_size=1000)
        for value in G.edges(data=True):
            if value[0] in ["MS", "MN", "MW", "ME", "MR", "MSW", "MSE", "MNW", "MNE"]:
                value = (value[1], value[0], value[2])

            if value[2]["weight"] < 0:
                nx.draw_networkx_edges(G, self.pos, edgelist=[value], width=value[2]["weight"],
                                       edge_color="r",  arrows=True, min_target_margin=25, arrowsize=10,
                                       connectionstyle='arc3,rad=0.2')
            else:
                nx.draw_networkx_edges(G, self.pos, edgelist=[value], width=value[2]["weight"],
                                       edge_color="g",  arrows=True, min_target_margin=25, arrowsize=10,
                                       connectionstyle='arc3,rad=0.2')
        # labels
        nx.draw_networkx_labels(G, self.pos, font_size=5, font_family="sans-serif")

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.title("score: " + str(self.score) )
        #print(self.genome)
        plt.tight_layout()
        if today==None:
            today = date.today().strftime("%Y-%m-%d")
            Path(f"./logs/{today}").mkdir(parents=False, exist_ok=True)
            biggest = 0
            for dir in glob.glob(f'./logs/{today}/*'):
                if os.path.isdir(dir):
                    value = int(dir.split("Run_")[1])
                    if value>biggest:
                        biggest = value

            run = f"/Run_{biggest}"
        Path(f"./logs/{today}/{run}").mkdir(parents=False, exist_ok=True)
        plt.savefig(f"./logs/{today}/{run}/Generation_{self.generation}.png", dpi=600)
        plt.close()
