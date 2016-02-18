from __future__ import division
import matplotlib.pyplot as plt
import random
import sys
import json
import os
from network import Network

dataFolder = "../error/circle/"
graphFolder = "../graphs/"

def generateMeanErrorGraph(errorFolder):

    iters = 5000
    print "Generating graphs for Mean Errors (%s) over %s iterations." %(errorFolder,iters)

    mainDirectory = dataFolder+errorFolder

    for directory in os.listdir(mainDirectory):
        
        fig, ax = plt.subplots()
        plt.axis([0,iters,0,0.27])

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

            plt.plot(range(len(avgMeanErrorList)),avgMeanErrorList, label=subDirectory)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels)
            plt.savefig(graphFolder+errorFolder+"_"+directory+".png")
   
def generateCircleGraph(data,output):
    plt.axis([0,20,0,20])

    for i in range(len(data)):
    
        x = data[i][0]
        y = data[i][1]

        

        inCircle = ((x-10)**2 + (y-10)**2) <= 49 
        print "Are coordinates %s, %s in circle? %s Output: %s" %(x,y,inCircle,output[i])

        if inCircle:
            if output[i] == 1:   
                pass
                # plt.plot(x,y, 'rs', markersize=5)

            if output[i] == 0:
               pass

        else:

            if output[i] == 1:   
               pass

            if output[i] == 0:
                plt.plot(x,y, 'bo', markersize=5)
              
    circle=plt.Circle((10,10),7,fill=False)
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.savefig('circle.png')



def main():
    generateMeanErrorGraph("learnRate")
    generateMeanErrorGraph("neurons")


if __name__ == '__main__':
    main()

