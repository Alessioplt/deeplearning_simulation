import glob
import os

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import date
class TimeSeriegenerator:
    def __init__(self, taille):
        self.x = []
        self.y = []
        self.taille = taille

    def restoreOldSim(self, x, y):
        self.x = x
        self.y = y

    def addValue(self, x, y, today=None, run=None):
        self.x.append(x)
        self.y.append(y)
        return self.update(today, run)


    def update(self, today=None, run=None):
        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.y)
        plt.title("Stats Simulation:" + str(self.taille) + " individus total")
        plt.xlabel("Generation N°")
        plt.ylabel("Nombres de survivants")
        print(today)
        if today == None:
            today = date.today().strftime("%Y-%m-%d")
            Path(f"./logs/{today}").mkdir(parents=False, exist_ok=True)
            biggest = 0
            for dir in glob.glob(f'./logs/{today}/*'):
                if os.path.isdir(dir):
                    value = int(dir.split("Run_")[1])
                    if value > biggest:
                        biggest = value
            if not self.x:
                biggest +=1
            run = f"/Run_{biggest}"
        Path(f"./logs/{today}/{run}").mkdir(parents=False, exist_ok=True)
        plt.savefig(f"./logs/{today}/{run}/_NuageDePoints.png", dpi=600)
        plt.close()
        return self.x, self.y, today, run
