import matplotlib.pyplot as plt
from network import Network
import json
import sys

dataFolder = "../data/"
weightsFolder = "../weights/"

MAXITER = 1000000
MINERR = 0.02
MIN = 0
MAX = 20

def printGraph():
    plt.axis([0,20,0,20])

    lines = readFile(fileName)

    for line in lines:
        x,y,value = line.split(" ")

        if (int(value) > 0):
            plt.plot(x, y, 'rs',  markersize=5)
        else:
            plt.plot(x, y, 'bo', markersize=5)

    circle=plt.Circle((10,10),7,fill=False)
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.savefig('graph.png')


def readFile(fileName):

    lines = []
    with open(fileName, "r") as f:
        lines = f.readlines()

    return lines

def normalizeInput(inputX,inputY,target):

    x = (inputX-MIN)/(MAX-MIN)
    y = (inputY-MIN)/(MAX-MIN)

    if (target == -1): 
        target = 0
    
    return (x,y,target)

def processData(data,datasetType):

    if (datasetType == 1):
        return (processCircleData(data),2)
    if (datasetType == 2):
        return (processIrisData(data),4)
    if (datasetType == 3):
        return (processLogicalOpData(data),2)

def processCircleData(data):

    processed = []

    for example in data:
        xValue,yValue,targetValue = example.split(" ")
        x,y,target = normalizeInput(float(xValue),float(yValue),int(targetValue))
        processed.append((x,y,target))

    return processed

def processIrisData(data):

    processed = []

    for example in data:
        sLenValue, sWidValue, pLenValue, pWidValue, irisValue = example.split(",")

        irisClass = 0

        if (irisValue.rstrip() == "Iris-setosa"):
            irisClass = 0
        elif (irisValue.rstrip() == "Iris-versicolor"):
            irisClass = 1
        elif (irisValue.rstrip() == "Iris-virginica"):
            irisClass = 1

        processed.append((float(sLenValue),float(sWidValue),float(pLenValue),float(pWidValue),irisClass))
    
    return processed

def processLogicalOpData(data):

    processed = []

    for example in data:
        x,y,target = example.split(" ")
        processed.append((int(x),int(y),int(target)))

    return processed

def main(argv):

    if len(argv) < 3: 
        print "python main.py <datasetType> <inputfile> <numHiddenLayerNeurons> <weightsFile>"
        print "Dataset Type:"
        print "\t1 -> circle"
        print "\t2 -> iris"
        print "\t3 -> logical operators"
        sys.exit()

    datasetType = int(argv[0])
    fileName = argv[1]
    numHidden = int(argv[2])

    datasetFolder = ""

    if (datasetType == 1):
        datasetFolder = "circle/"
    elif (datasetType == 2):
        datasetFolder = "iris/"
    elif (datasetType == 3):
        datasetFolder = "logicalOperators/"

    path = dataFolder+datasetFolder+fileName
    f = open(path,'r')

    fileData = readFile(path)
    data,numInput = processData(fileData,datasetType)
    
    iteration = 0
    totalError = 2000
    numOuter = 1

    network = Network(numInput,numHidden,numOuter)

    if len(argv) == 4:

        path = weightsFolder+datasetFolder+"weights_"+str(numHidden)+"_"+fileName
        
        with open(path,'r') as weightsFile:
            weights = json.load(weightsFile)

        network.setWeights(weights)


    #TODO Verify previous error to see if it changes
    while (totalError != 0 and totalError > MINERR and iteration < MAXITER):

        print "Iteration: %s" %(iteration)
        totalError = 0
        totalError = network.train(data)
        iteration += 1
    
    network.printWeights()

    weights = network.getWeights()

    path = weightsFolder+datasetFolder+"weights_"+str(numHidden)+"_"+fileName
    with open(path,'w') as weightsFile:
        json.dump(weights,weightsFile)


    # fileData = readFile(dataFolder+datasetFolder+"or.txt")
    # data,numInput = processData(fileData,datasetType)

    # network2.classify(data)

if __name__ == '__main__':
    main(sys.argv[1:])