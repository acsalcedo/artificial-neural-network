import matplotlib.pyplot as plt
from network import Network
import json
import sys, os.path
import time
import getopt

dataFolder = "../data/"
weightsFolder = "../weights/"
errorFolder = "../error/"

MAXITER = 10000
MINERR = 0.001
MIN = 0
MAX = 20

def printGraph(filePath):
    plt.axis([0,20,0,20])

    lines = readFile(filePath)

    countCircle = 0
    countSquare = 0

    for line in lines:
        x,y,value = line.split(" ")

        if (int(value) > 0):
            countSquare += 1
            plt.plot(x, y, 'rs',  markersize=5)
        else:
            countCircle += 1
            plt.plot(x, y, 'bo', markersize=5)

    circle=plt.Circle((10,10),7,fill=False)
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.savefig('graph.png')
    print "countCircle: %s countSquare: %s" %(countCircle,countSquare)


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
        return (processCircleData(data),2,1)
    if (datasetType == 2):
        return (processIrisData(data),4,1)
    if (datasetType == 3):
        return (processIrisData2(data),4,3)
    if (datasetType == 4):
        return (processLogicalOpData(data),2,1)
    if (datasetType == 5):
        return (processLogicalOpData2(data),3,1)

def processCircleData(data):

    processed = []

    for example in data:
        xValue,yValue,targetValue = example.split(" ")
        x,y,target = normalizeInput(float(xValue),float(yValue),int(targetValue))
        processed.append((x,y,[target]))

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

        processed.append((float(sLenValue),float(sWidValue),float(pLenValue),float(pWidValue),[irisClass]))
    
    return processed

def processIrisData2(data):

    processed = []

    for example in data:
        sLenValue, sWidValue, pLenValue, pWidValue, irisValue = example.split(",")

        irisClass = 0

        if (irisValue.rstrip() == "Iris-setosa"):
            irisClass = [1,0,0]
        elif (irisValue.rstrip() == "Iris-versicolor"):
            irisClass = [0,1,0]
        elif (irisValue.rstrip() == "Iris-virginica"):
            irisClass = [0,0,1]

        processed.append((float(sLenValue),float(sWidValue),float(pLenValue),float(pWidValue),irisClass))
    
    return processed

def processLogicalOpData(data):

    processed = []

    for example in data:
        x,y,target = example.split(" ")
        processed.append((int(x),int(y),[int(target)]))

    return processed

def processLogicalOpData2(data):

    processed = []

    for example in data:
        x,y,z,target = example.split(" ")
        processed.append((int(x),int(y),int(z),[int(target)]))

    return processed

def printError():
    print "\npython main.py -t <datasetType> -i <inputDataFile> -n <numHiddenLayerNeurons> -w <weightsFile> -r <learnRate>"
    print "\nDataset Type:"
    print "\t1 -> circle"
    print "\t2 -> iris"
    print "\t3 -> iris with three classes" 
    print "\t4 -> logical operators"
    print "\nWeights file and learn rate are optional."
    print
    sys.exit(2)

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"t:i:n:w:r:",["datasetType=","infile=","numHidden=","weightsFile=","rate="])
    except getopt.GetoptError:
        print "\nIncorrect call. Please try again."
        printError()

    datasetType = None
    numHidden = None
    weightsFile = None
    learnRate = 0.05

    for opt, arg in opts:
        if opt in ("-t", "--datasetType"):
            datasetType = int(arg)
        elif opt in ("-i", "--infile"):
            fileName = str(arg)
        elif opt in ("-n", "--numHidden"):
            numHidden = int(arg)
        elif opt in ("-w", "--weightsFile"):
            weightsFile = str(arg)
        elif opt in ("-r", "--rate"):
            learnRate = float(arg)

    if numHidden is None:
        print "\nPlease enter the number of neurons in the hidden layer."
        printError()

    if datasetType is None:
        print "\nPlease enter the type of the data set."
        printError()

    datasetFolder = ""

    if (datasetType == 1):
        datasetFolder = "circle/"
    elif (datasetType == 2 or datasetType == 3):
        datasetFolder = "iris/"
    elif (datasetType == 4):
        datasetFolder = "logicalOperators/"

    filePath = dataFolder+datasetFolder+fileName
    fileExists = os.path.isfile(filePath)

    if fileExists:
        f = open(filePath,'r')
    else:
        print "\nThe given input file '%s' doesn't exist.\n" %(filePath)
        sys.exit()

    fileData = readFile(filePath)
    data,numInput,numOuter = processData(fileData,datasetType)
    
    iteration = 0
    totalError = 2000

    network = Network(numInput,numHidden,numOuter,learnRate)

    if weightsFile is not None: 

        filePath = weightsFolder+datasetFolder+weightsFile
        
        with open(filePath,'r') as f:
            weights = json.load(f)

        network.setWeights(weights)

    totalErrors = []

    #TODO Verify previous error to see if it changes
    # while (totalError != 0 and totalError > MINERR and iteration < MAXITER):

    global MAXITER

    if (learnRate == 0.2):
        MAXITER = 20000
    elif (learnRate == 0.1):
        MAXITER = 25000
    elif (learnRate == 0.05):
        MAXITER = 40000
    elif (learnRate == 0.01):
        MAXITER = 50000

    print MAXITER

    while (iteration < MAXITER):
        # print "Iteration: %s" %(iteration)
        totalError = 0
        totalError = network.train(data)
        totalErrors.append(totalError)
        iteration += 1
    
    # network.printWeights()

    timestr = time.strftime("%Y%m%d%H%M%S")
    errorName = "error_neurons"+str(numHidden)+"_rate"+str(learnRate)+"_"+timestr+"_"
    filePath = errorFolder+datasetFolder+errorName+fileName
    
    with open(filePath,'w') as errorFile:
        json.dump(totalErrors,errorFile)    

    weights = network.getWeights()

    # weightStr = ""
    # if datasetType == 3:
    #     weightStr= "2_weights_"
    # else:
    #     weightStr= "weights_"

    weightStr = "weights_neurons"+str(numHidden)+"_rate"+str(learnRate)+"_"+timestr+"_"

    filePath = weightsFolder+datasetFolder+weightStr+fileName
    with open(filePath,'w') as weightsFile:
        json.dump(weights,weightsFile)

if __name__ == '__main__':
    main(sys.argv[1:])