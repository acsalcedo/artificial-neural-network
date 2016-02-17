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

        for i in range(len(errors)):
        # for i in range(5000):
            iterList.append(i)
            errorList.append(errors[i])

        plt.plot(iterList,errorList)

        plt.savefig('plot.png')


def meanError():


    for directory in os.listdir(dataFolder):
        
        totalIters = 0
        meanError = 0

        print directory

        folder = dataFolder+directory
        
        for fileName in os.listdir(folder):

            f = open(os.path.join(folder, fileName), "r")

            errors = json.load(f)

            for i in range(len(errors)):
                meanError += errors[i]

            totalIters += len(errors)

        meanError = meanError / totalIters

        print meanError
        

# generateGraph()
meanError()