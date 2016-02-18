from __future__ import division
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
        
        fig, ax = plt.subplots()
        plt.axis([0,5000,0,0.27])

        print directory

        folder = dataFolder+directory
        minError = 1

        for subDirectory in os.listdir(folder):

            print subDirectory

            subFolder = folder+"/"+subDirectory
            totalIters = 0
            meanError = 0

            allErrorList = []

            for fileName in os.listdir(subFolder):
                f = open(os.path.join(subFolder, fileName), "r")

                errors = json.load(f)

                errorList = []

                for i in range(5000):
                    if errors[i] < minError:
                        minError = errors[i]

                    meanError += errors[i]
                    errorList.append(errors[i])

                totalIters += len(errors)

                allErrorList.append(errorList)

            avgList = [sum(e)/len(e) for e in zip(*allErrorList)]

            # print avgList
            # meanError = meanError / totalIters

            # print minError
            # print meanError

            plt.plot(range(len(avgList)),avgList, label=subDirectory)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels)
            plt.savefig(directory+".png")
        

# generateGraph()
meanError()