import matplotlib.pyplot as plt
import random
import sys
import json
import os

dataFolder = "../error/circle/"
def generateGraph():
    


    for fileName in os.listdir(dataFolder):

        f = open(os.path.join(dataFolder, fileName), "r")

        errors = json.load(f)
        iterList,errorList = [], []

        # for i in range(len(errors)):
        for i in range(5000):
            iterList.append(i)
            errorList.append(errors[i])

        plt.plot(iterList,errorList)

        plt.savefig('plot.png')

generateGraph()