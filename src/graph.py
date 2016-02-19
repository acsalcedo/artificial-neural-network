from __future__ import division
import matplotlib.pyplot as plt
import random
import sys
import json
import os
from network import Network
import matplotlib.patches as mpatches

circleDataFolder = "../error/circle/"
irisDataFolder = "../error/iris/"
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

    mainDirectory = circleDataFolder+errorFolder

    if (errorFolder == "neurons"):
        title = "Neuronas - Error Cuadratico Medio"
        titleLegend = "# Neuronas"
    else:
        title = "Tasa de Aprendizaje - Error Cuadratico Medio"
        titleLegend = "Tasa de Aprendizaje"

    for directory in os.listdir(mainDirectory):
        
        fig, ax = plt.subplots()
        plt.title(title)
        plt.axis([0,iters,0,0.27])
        ax.set_xlabel('Iteracion')
        ax.set_ylabel('Error')

        print "Currently in directory: %s" %(directory)

        folder = mainDirectory+"/"+directory
        minMeanError = 1
        totalMeanErrorList = []

        for subDirectory in os.listdir(folder):

            print "Currently generating graph for: %s" %(subDirectory)

            subFolder = folder+"/"+subDirectory
            totalIterations = 0
            meanErrorListor = 0

            meanErrorListList = []

            for fileName in os.listdir(subFolder):
                f = open(os.path.join(subFolder, fileName), "r")

                errors = json.load(f)

                meanErrorList = []
                meanError = 0

                for i in range(iters):

                    if errors[i] < minMeanError:
                        minMeanError = errors[i]

                    meanError += errors[i]
                    meanErrorList.append(errors[i])

                totalIterations += iters

                meanErrorListList.append(meanErrorList)

            meanError = meanError / totalIterations

            totalMeanErrorList.append(meanError)

            #Finds the average of mean errors for each iteration.
            avgMeanErrorList = [sum(e)/len(e) for e in zip(*meanErrorListList)]

            plt.plot(range(len(avgMeanErrorList)),avgMeanErrorList, label=subDirectory, linestyle=linestyles[pos], linewidth=2)
            pos = (pos + 1) % len(linestyles)
        
        handles, labels = ax.get_legend_handles_labels()
        
        if (errorFolder == "learnRate"):
            labels = getNewLabels(labels)

        ax.legend(handles, labels, title=titleLegend)

        name = graphFolder+errorFolder+"_"+directory

def generateIrisGraph():

    iters = 200
    pos = 0
    linestyles = ['-', '--', '-.', ':']
    
    mainDirectory = irisDataFolder+"all/"

    fig, ax = plt.subplots()
    plt.title("Neuronas - Error Cuadratico Medio - Iris")
    begin = 0
    plt.axis([begin,iters,0,0.3])
    ax.set_xlabel('Iteracion')
    ax.set_ylabel('Error')

    minMeanError = 1
    totalMeanErrorList = []
    
    for fileName in os.listdir(mainDirectory):
        
        f = open(os.path.join(mainDirectory, fileName), "r")
        lhs,rhs = fileName.split("neurons")
        neuronNum, rest = rhs.split("_",1)
        errors = json.load(f)
        meanErrorList = []

        for i in range(iters):
            meanErrorList.append(errors[i])

        plt.plot(range(begin,200),meanErrorList[begin:], label=neuronNum, linestyle=linestyles[pos], linewidth=2)
        pos = (pos + 1) % len(linestyles)
        
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title="# Neurons")
    plt.savefig(graphFolder+"iris.png")

#Generation of bar graphs of point errors.
def generatBarGraphError(dataType):

    error1, error2 = [],[]
    #Given 
    if dataType == "given":
        error1 = [1982,28,42,36,33,29,46,38,43]
        error2 =[602,100,86,103,32,35,24,25,12]
    #Generated
    else:
        error1 = [2354,41,48,44,38,30,36,33,42]
        error2 = [301,107,53,56,73,47,55,38,54]
    meanError = []

    for i in range(len(error1)):
        meanError.append((error1[i]+error2[i])/10000) 

    plt.clf()
    barGraph = plt.bar(range(2,11), meanError)
    plt.xlabel('Neuronas')
    plt.ylabel('Error')
    plt.title('Error de la Clasificacion de Datos')
    plt.grid(True)
    plt.savefig(graphFolder+dataType+"_bargraph.png")


def generateCircleGraph(data,output):
    plt.axis([0,20,0,20])
    fig, ax = plt.subplots()
    wrongCircle = 0
    wrongSquare = 0

    for i in range(len(data)):
    
        x = data[i][0]
        y = data[i][1]

        inCircle = ((x-10)**2 + (y-10)**2) <= 49 

        #Circle output
        if output[i] == 0:
            #If classified as circle, but is square
            if not inCircle:

                wrongCircle += 1
                plt.plot(x,y, 'rs', label="Pto. cuadrado en circulo", markersize=5)
        else:
            if inCircle:
                wrongSquare += 1
                plt.plot(x,y, 'bo', label="Pto. circulo en cuadrado", markersize=5)

              
    classes = ['Err. Cuadrado','Err. Circulo']
    class_colours = ['r','b']
    recs = []
    for i in range(0,len(class_colours)):
        recs.append(mpatches.Circle((0,0),1,fc=class_colours[i]))
    plt.legend(recs,classes,fontsize=9)
    
    print "\nCircle points classified as square points: %s" %(wrongCircle)
    print "Square points classified as circle points: %s" %(wrongSquare)
    circle=plt.Circle((10,10),7,fill=False)
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.grid(True)
    plt.title("Puntos Mal Clasificados")
    plt.savefig(graphFolder+"circle.png")


def getIrisClass(example,dataType):

    sLenValue, sWidValue, pLenValue, pWidValue, irisValue = example
    
    if dataType == 2:
        return irisValue[0]

    return irisValue

def generateIris(data,output,dataType):

    right = 0
    wrong = 0

    for i in range(len(data)):

        irisClass = getIrisClass(data[i],dataType)

        if irisClass == output[i]:
            right += 1
        else:
            wrong += 1


    print "\nNumber of Iris correctly classified: %s" %(right)
    print "Number of Iris incorrectly classified: %s" %(wrong)
