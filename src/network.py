import matplotlib.pyplot as plt
import random
import math

fileName = "../data/datos_P1_RN_EM2016_n500.txt"

LEARNRATE = 0.05
MAXITER = 1000000
MINERR = .002
MIN = 0
MAX = 20

def readFile(fileName):

    lines = []
    with open(fileName, "r") as f:
        lines = f.readlines()

    return lines

def getRandom():
    return random.random()*0.5

class Neuron:

    def __init__(self,id,numInput):
        self.id = id
        self.error = 0
        self.output = 0
        self.input = []
        self.weights = []
        self.threshold = getRandom()
        
        for i in range(numInput):
            self.weights.append(getRandom())
    
    def getId(self):
        return self.id

    def getThreshold(self):
        return self.threshold

    def setInput(self,inputs):
        self.input = inputs

    def updateWeights(self):

        self.threshold += LEARNRATE*self.error

        for i in range(len(self.input)):
            self.weights[i] += LEARNRATE*self.error*self.input[i]
    
    def calculateOutput(self):

        net = self.threshold
        
        for i in range(len(self.input)):
            net += self.weights[i] * self.input[i]

        output = 1 / (1 + math.exp(-net))
        self.output = output
        return output

    def getOutput(self):
        return self.output

    def getError(self):
        return self.error

    def setError(self,error):
        self.error = error

    def calculateOuterError(self,target):
        self.error = self.output*(1-self.output)*(target-self.output)
        return self.error

    def calculateErrorSum(self,pos):
        return self.weights[pos] * self.error

    
class NeuronLayer:

    def __init__(self,initId,numNeurons,numInput):
        self.neurons = []

        for i in range(numNeurons):
            self.neurons.append(Neuron(i+initId,numInput))

    def setInput(self,inputs):
        for neuron in self.neurons:
            neuron.setInput(inputs)

    def printWeights(self):
        for neuron in self.neurons:
            print "Neuron: %s - " %(neuron.getId()),
            print "Weights: %s" %(neuron.getThreshold()),
            for weight in neuron.weights:
                print "%s " %(weight),
            print
    
    def calculateOutputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculateOutput())

        return outputs

    def getOutput(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.getOutput())

        return outputs
    
    def calculateOuterErrors(self,target):
        errors = []
        for neuron in self.neurons:
            errors.append(neuron.calculateOuterError(target))

        return errors

    def updateWeights(self):
        for neuron in self.neurons:
            neuron.updateWeights()

def normalizeInput(inputX,inputY,target):

    x = (inputX-MIN)/(MAX-MIN)
    y = (inputY-MIN)/(MAX-MIN)

    if (target == -1): 
        target = 0
    
    return (x,y,target)

def train():

    totalError = 1
    iteration = 0
    numHidden = 10
    numOuter = 1
    numInput = 2
    
    data = readFile(fileName)

    #TESTING AND
    # data = [(0,0,0),(0,1,0),(1,0,0),(1,1,1)]
    
    hiddenLayer = NeuronLayer(0,numHidden,numInput)
    outerLayer = NeuronLayer(numHidden,numOuter,numHidden)

    hiddenLayer.printWeights()
    outerLayer.printWeights()

    while (totalError != 0 and totalError > MINERR and iteration < MAXITER):

        print "Iteration: %s" %(iteration)
        totalError = 0

        for example in data:

            xValue,yValue,targetValue = example.split(" ")

            x,y,target = normalizeInput(float(xValue),float(yValue),int(targetValue))

            #TESTING AND
            # x,y,target = example
            
            inputs = [x,y]

            hiddenLayer.setInput(inputs)            
            hiddenOutputs = hiddenLayer.calculateOutputs()

            outerLayer.setInput(hiddenOutputs)
            outerOutputs = outerLayer.calculateOutputs()

            errorsOuter = outerLayer.calculateOuterErrors(target)

            for neuron in hiddenLayer.neurons:

                output = neuron.getOutput()
                errorHidden = output*(1-output)
                errorSum = 0

                for outerNeuron in outerLayer.neurons:
                    errorSum += outerNeuron.calculateErrorSum(neuron.getId())

                errorHidden = errorHidden * errorSum

                neuron.setError(errorHidden)
            
            hiddenLayer.updateWeights()
            outerLayer.updateWeights()

            error = 0

            for o in outerLayer.getOutput():
                error += 0.5*(target-o)**2

            totalError += error
            # print "Outer output: %s - Target: %s - Error: %s" %(outerLayer.getOutput(),target,error)
    
        print "Error: %s\n" %(totalError)    
        iteration += 1

    print "\nHIDDEN LAYER WEIGHTS:"
    hiddenLayer.printWeights()

    print "\nOUTER LAYER WEIGHTS:"
    outerLayer.printWeights()

train()