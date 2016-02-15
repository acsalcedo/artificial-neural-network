import random
import math

LEARNRATE = 0.05

def getRandom():
    return random.random()*0.5

class Neuron:

    def __init__(self,id,numInput):
        self.id = id
        self.error = 0
        self.output = 0
        self.input = []
        self.weights = []

        #Initialization of the weights.
        self.threshold = getRandom()
        for i in range(numInput):
            self.weights.append(getRandom())
    
    def getId(self):
        return self.id

    def setInput(self,inputs):
        self.input = inputs

    def getThreshold(self):
        return self.threshold

    def getWeights(self):
        w = self.weights
        w.append(self.threshold)
        return w
    
    def setWeights(self,weights):
        self.weights = weights[:-2]
        self.threshold = weights[-1]
    
    def updateWeights(self):
        self.threshold += LEARNRATE*self.error
        
        for i in range(len(self.input)):
            self.weights[i] += LEARNRATE*self.error*self.input[i]

    def getOutput(self):
        return self.output

    def calculateOutput(self):
        net = self.threshold
        
        for i in range(len(self.input)):
            net += self.weights[i] * self.input[i]

        output = 1 / (1 + math.exp(-net))
        self.output = output
        return output

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
    
    def getWeights(self):
        weights = []
        for neuron in self.neurons:
            weights.append(neuron.getWeights())
        return weights

    def setWeights(self,weights):
        for i in range(len(self.neurons)):
            self.neurons[i].setWeights(weights[i])

    def updateWeights(self):
        for neuron in self.neurons:
            neuron.updateWeights()
    
    def printWeights(self):
        for neuron in self.neurons:
            print "Neuron: %s - " %(neuron.getId()),
            print "Weights: %s" %(neuron.getThreshold()),
            for weight in neuron.weights:
                print "%s " %(weight),
            print
    
    def getOutput(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.getOutput())
        return outputs
    
    def calculateOutputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculateOutput())
        return outputs

    def calculateOuterErrors(self,target):
        errors = []
        for neuron in self.neurons:
            errors.append(neuron.calculateOuterError(target))
        return errors

class Network:

    def __init__(self,numInput,numHidden,numOuter):
        self.numHidden = numHidden
        self.numOuter = numOuter
        
        self.hiddenLayer = NeuronLayer(0,numHidden,numInput)
        self.outerLayer = NeuronLayer(numHidden,numOuter,numHidden)

    def getWeights(self):
        weights = []
        weights.append(self.hiddenLayer.getWeights())
        weights.append(self.outerLayer.getWeights())
        return (self.hiddenLayer.getWeights(),self.outerLayer.getWeights())
    
    def setWeights(self,weights):
        hiddenWeights,outerWeights = weights
        self.hiddenLayer.setWeights(hiddenWeights)
        self.outerLayer.setWeights(outerWeights)
    
    def printWeights(self):
        print "\nHIDDEN LAYER WEIGHTS:"
        self.hiddenLayer.printWeights()
        print "\nOUTER LAYER WEIGHTS:"
        self.outerLayer.printWeights()
    
    def train(self,data):
        totalError = 0

        for example in data:

            inputs = []
            for i in example[:-1]:
                inputs.append(i)

            target = example[-1]
            
            self.hiddenLayer.setInput(inputs)            
            hiddenOutputs = self.hiddenLayer.calculateOutputs()

            self.outerLayer.setInput(hiddenOutputs)
            outerOutputs = self.outerLayer.calculateOutputs()

            errorsOuter = self.outerLayer.calculateOuterErrors(target)

            for neuron in self.hiddenLayer.neurons:

                output = neuron.getOutput()
                errorHidden = output*(1-output)
                errorSum = 0

                for outerNeuron in self.outerLayer.neurons:
                    errorSum += outerNeuron.calculateErrorSum(neuron.getId())

                errorHidden = errorHidden * errorSum

                neuron.setError(errorHidden)
            
            self.hiddenLayer.updateWeights()
            self.outerLayer.updateWeights()

            error = 0

            for o in self.outerLayer.getOutput():
                error += (target-o)**2

            totalError += error
            # print "Outer output: %s - Target: %s - Error: %s" %(outerLayer.getOutput(),target,error)
    
        totalError *= 0.5
        print "Error: %s\n" %(totalError)

        return totalError

    def classify(self,data):

        for example in data:

            inputs = []
            for i in example[:-1]:
                inputs.append(i)

            self.hiddenLayer.setInput(inputs)            
            hiddenOutputs = self.hiddenLayer.calculateOutputs()

            self.outerLayer.setInput(hiddenOutputs)
            outerOutputs = self.outerLayer.calculateOutputs()

            for o in outerOutputs:
                print o
                # TODO

