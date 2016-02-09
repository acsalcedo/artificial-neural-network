import matplotlib.pyplot as plt
import random
import math

fileName = "../data/datos_P1_RN_EM2016_n2000.txt"

class Neuron:

    def __init__(self, id, output, error):
        self.id = id
        self.output = output
        self.error = error

    def getId(self):
        return self.id

    def getOutput(self):
        return self.output

    def getError(self):
        return self.error

    def setError(self,error):
        self.error = error

    def __str__(self):
        return "Neuro:\n ID: %s\n Output: %s\n Error:%s" %(self.id,self.output,self.error)

def readFile(fileName):

    lines = []

    with open(fileName, "r") as f:
        lines = f.readlines()

    return lines
    

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


# como se calcula el error del while?

error = 1
minError = 0.02
maxIterations = 500
z = 0
data = readFile(fileName)
hiddenNeurons = 4
inputNeurons = 2
outputNeuron = 1
learningRate = 0.05
totalNeurons = hiddenNeurons + inputNeurons + outputNeuron
#random.random()*0.5
weightMatrix = [[0.2 for x in range(totalNeurons+1)] for x in range(totalNeurons+1)] 

print weightMatrix


while (error != 0 and error > minError and z < maxIterations):
    
    for example in data:
        
        neurons = []
        xValue,yValue,targetValue = example.split(" ")

        x = float(xValue)
        y = float(yValue)
        target = int(targetValue)
        # inputArray = [float(x),float(y)]

        for i in range(inputNeurons+1,inputNeurons+hiddenNeurons+1):
        
            net = weightMatrix[1][i] * x +weightMatrix[2][i]* y + weightMatrix[0][i]
            output = 1 / (1 + math.exp(-net))

            # print "Hidden layer net: %s" %(net)
            neuron = Neuron(i,output,-1)
            neurons.append(neuron)

        outerNeurons = []

        for i in range(inputNeurons+hiddenNeurons+1,totalNeurons+1):

            net = weightMatrix[0][i]

            for neuron in neurons:
                net += weightMatrix[neuron.getId()][i] * neuron.getOutput()

                # print "Neuron id: %s i: %s net: %s" %(neuron.getId(),i,net)

            output = 1 / (1 + math.exp(-net))

            # print "Outer layer output: %s" %(output)

            errorOuter = output*(1-output)*(target-output)

            neuron = Neuron(i,output,errorOuter)

            outerNeurons.append(neuron)

        for neuron in neurons:

            errorNeuron = neuron.getOutput()*(1-neuron.getOutput())
            errorSum = 0

            for outerNeuron in outerNeurons:

                errorSum += outerNeuron.getError() * weightMatrix[neuron.getId()][outerNeuron.getId()]

            errorNeuron = errorNeuron*errorSum
                
            neuron.setError(errorNeuron)

            for outerNeuron in outerNeurons:

                weightMatrix[neuron.getId()][outerNeuron.getId()] += learningRate*outerNeuron.getError()*neuron.getOutput()
                weightMatrix[0][outerNeuron.getId()] +=  learningRate*outerNeuron.getError()

                print "Outer neuron output: %s target: %s" %(outerNeuron.getOutput(),target)
        
            weightMatrix[1][neuron.getId()] +=  learningRate*neuron.getError()*x 
            weightMatrix[2][neuron.getId()] +=  learningRate*neuron.getError()*y
            weightMatrix[0][neuron.getId()] +=  learningRate*neuron.getError()

            # print "Hidden neuron layer output: %s" %(neuron.getOutput())

    z += 1










