from __future__ import division
import matplotlib.pyplot as plt
import random
import sys
import json
import os
from network import Network

dataFolder = "../error/circle/"
graphFolder = "../graphs/"

def getNewLabels(labels):

    newLabels = []
    for label in labels:
        newLabels.append(label.replace("r",""))
    return newLabels

def generateMeanErrorGraph(errorFolder):

    iters = 5000
    pos = 0
    linestyles = ['-', '--', '-.', ':']
    print "Generating graphs for Mean Errors (%s) over %s iterations." %(errorFolder,iters)

    mainDirectory = dataFolder+errorFolder

    if (errorFolder == "neurons"):
        title = "Neuronas - Error Cuadratico Medio"
        titleLegend = "# Neuronas"
    else:
        title = "Taza de Aprendizaje - Error Cuadratico Medio"
        titleLegend = "Taza de Aprendizaje"

    for directory in os.listdir(mainDirectory):
        
        fig, ax = plt.subplots()
        plt.title(title)
        plt.axis([0,iters,0,0.27])
        ax.set_xlabel('Iteracion')
        ax.set_ylabel('Error')

        print "Currently in directory: %s" %(directory)

        folder = mainDirectory+"/"+directory
        minMeanError = 1

        for subDirectory in os.listdir(folder):

            print "Currently generating graph for: %s" %(subDirectory)

            subFolder = folder+"/"+subDirectory
            totalIterations = 0
            meanError = 0

            meanErrorListList = []

            for fileName in os.listdir(subFolder):
                f = open(os.path.join(subFolder, fileName), "r")


                errors = json.load(f)

                meanErrorList = []

                for i in range(iters):

                    if errors[i] < minMeanError:
                        minMeanError = errors[i]

                    meanError += errors[i]
                    meanErrorList.append(errors[i])

                totalIterations += len(errors)

                meanErrorListList.append(meanErrorList)

            #Finds the average of mean errors for each iteration.
            avgMeanErrorList = [sum(e)/len(e) for e in zip(*meanErrorListList)]

            plt.plot(range(len(avgMeanErrorList)),avgMeanErrorList, label=subDirectory, linestyle=linestyles[pos], linewidth=2)
            pos = (pos + 1) % len(linestyles)
        
        handles, labels = ax.get_legend_handles_labels()
        
        if (errorFolder == "learnRate"):
            labels = getNewLabels(labels)

        ax.legend(handles, labels, title=titleLegend)

        plt.savefig(graphFolder+errorFolder+"_"+directory+".png")
   
def generateCircleGraph(data,output):
    plt.axis([0,20,0,20])

    for i in range(len(data)):
    
        x = data[i][0]
        y = data[i][1]

        

        inCircle = ((x-10)**2 + (y-10)**2) <= 49 
        print "Are coordinates %s, %s in circle? %s Output: %s" %(x,y,inCircle,output[i])


        if output[i] == 0:

            if not inCircle:
                plt.plot(x,y, 'rs', markersize=5)
        else:

            if inCircle:
                plt.plot(x,y, 'go', markersize=5)
        # if inCircle:
        #     if output[i] == 1:   
        #         pass
        #         # plt.plot(x,y, 'rs', markersize=5)

        #     if output[i] == 0:
        #        pass

        # else:

        #     if output[i] == 1:   
        #        pass

        #     if output[i] == 0:
        #         plt.plot(x,y, 'bo', markersize=5)
              
    circle=plt.Circle((10,10),7,fill=False)
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.savefig('circle.png')



def main():
    generateMeanErrorGraph("learnRate")
    generateMeanErrorGraph("neurons")


if __name__ == '__main__':
    main()

