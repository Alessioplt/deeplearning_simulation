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
        plt.title("Stats Simulation:" + str(taille) + " individus total")
        plt.xlabel("Generation N°")
        plt.ylabel("Nombres de survivants")

        self.update()

    def addValue(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.update()


    def update(self):
        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.y)
        today = date.today().strftime("%Y-%m-%d")
        Path(f"./logs/{today}").mkdir(parents=False, exist_ok=True)
        biggest = 0
        for dir in glob.glob(f'./logs/{today}/*'):
            if os.path.isdir(dir):
                value = int(dir.split("Run_")[1])
                if value > biggest:
                    biggest = value
        run = f"/Run_{biggest}"
        Path(f"./logs/{today}/{run}").mkdir(parents=False, exist_ok=True)
        plt.savefig(f"./logs/{today}/{run}/_NuageDePoints.png", dpi=600)
        plt.close()
