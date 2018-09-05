# test everything, see stuff below--make sure all types are numpy arrays
# make activation function able to be changed, and learning rates, and inverse activation functions
# write comments about what each variable is...etc. and how to change them and what the functions do
# make sure no weights are 0
# test my ideas
# optimize my code

# fix bias node back to some average from 1.0
# fix numInputNodes-1 to numInputNodes in np.random
# fix learning rate of bias node



# make sure all the num nodes stuff is correct due to bias nodes and weights
# make sure all the variables make sense (like I didn't write a when I meant b)
# make sure all variables updated
# add functionality to make changes to individial learning rates and activation functions/derivatives/inverse activation functions
# add backquery functionality for any layer
# is there some reason why adding a bias node decreases accuracy...?

import numpy as np
import scipy.special
import scipy.misc
import matplotlib.pyplot
import time
import copy

# Node verified correct
class Node:
    # learning rate is a float between 0 and 1
    def __init__(self, learningRate, activationFunction, inverseActivationFunction):
        self.learningRate = float(learningRate)
        self.activationFunction = activationFunction
        self.inverseActivationFunction = inverseActivationFunction
    def updateLearningRate(self, newLearningRate):
        fNewLearningRate = float(newLearningRate)
        self.learningRate = fNewLearningRate

# InputLayer verified correct
class InputLayer:
    # numNodes is an int which is the number of nodes in the input layer, not including the bias node
    # nextLayer is the layer which is the it inputs to
    # nodeList is a list of input nodes
    # the bias node should always be the last one in the list
    def __init__(self, numNodes, nextLayer, nodeList):
        # for bias node
        self.numNodes = numNodes + 1
        self.numNonBiasNodes = numNodes
        self.nextLayer = nextLayer
        # myBiasNode = Node(0.1, lambda x : 0.001, lambda x: 0.001)
        self.nodeList = nodeList

    # calculateOutputs will return the output WITHOUT the bias node
    def calculateOutputs(self, inputs):
        return np.array(np.array(inputs), ndmin=2).T

# verified OutputLayer
class OutputLayer:
    # numNodes is the number of nodes in the output layer
    # prevLayer is the layer which is gets input from
    # numInputNodes is the number of nodes in the prevLayer
    # nodeList is a list of nodes in the output layer
    # weightList is a list of lists which represents weight. See layer initialization function
    # for the conventions
    def __init__(self, numNodes, prevLayer, numInputNodes, nodeList, weightList):
        self.numNodes = numNodes
        self.numNonBiasNodes = numNodes
        self.prevLayer = prevLayer
        self.numInputNodes = numInputNodes
        self.nodeList = nodeList
        self.weightList = weightList

    # calculateOutputs will return the output WITHOUT the bias node
    def calculateOutputs(self, inputs):
        # error checking
        layer_bias_inputs = np.append(inputs, np.array(1.0))

        if len(layer_bias_inputs) != self.numInputNodes:
            print(len(layer_bias_inputs))
            print(self.numInputNodes)
            print("Wrong number of inputs; failed")
            exit(1)
        formattedInputs = np.array(layer_bias_inputs, ndmin=2).T
        layer_inputs = np.dot(self.weightList, formattedInputs)
        activationFunctions = []
        for node in self.nodeList:
            activationFunctions.append(node.activationFunction)
        layer_outputs = np.array([f(i) for f, i in zip(activationFunctions, layer_inputs)])
        return layer_outputs


# verified correct
class HiddenLayer:
    # numNodes is an int which is the number of nodes, not including the bias node
    # prevLayer is another layer which is the one which it inputs to
    # nextLayer is another layer which is the one it outputs to
    # weightList is a list of lists. The first list in the list of lists are the weights for the first node in
    # this layer, in order
    # of the nodes in the prev layer, and so on and so forth. The bias node obviously will not have an
    # input in the list of lists
    # nodeList should not contain the bias node, at least in the input
    # neither will self.nodeList
    def __init__(self, numNodes, prevLayer, nextLayer, weightList, numInputNodes, nodeList):
        self.fixedLayer = True
        for node in nodeList:
            if node.learningRate != 0.0:
                self.fixedLayer = False
        # for bias node
        self.numNodes = numNodes + 1
        self.numNonBiasNodes = numNodes
        self.prevLayer = prevLayer
        self.nextLayer = nextLayer
        self.weightList = weightList
        self.numInputNodes = numInputNodes
        # myBiasNode = Node(0.1, (lambda x : 0.001), (lambda x: 0.001))
        self.nodeList = nodeList

    # whichNode is an int describing which node to delete
    # must be between 0 and numNodes - 2, incusive
    # will do notihng if try to delete the last node in the layer
    def deleteNode(self, whichNode):
        # error checking
        if self.numNonBiasNodes <= 1:
            print("You tried to delete the last node in this hidden layer; failed. Try calling delete later instead.")
            exit(1)
        if whichNode < 0 or whichNode >= self.numNonBiasNodes:
            print("You passed an invalid argument; failed")
            exit(1)

        # modifying this layer
        del self.weightList[whichNode]
        del self.nodeList[whichNode]
        self.numNodes -= 1
        self.numNonBiasNodes -= 1

        # modifying the next layer
        nextLayer = self.nextLayer
        nextLayer.numInputNodes -= 1
        nextLayerWeightList = nextLayer.weightList
        for nodeWeights in nextLayerWeightList:
            del nodeWeights[whichNode]

        # updating fixedLayer
        allZero = True
        for node in self.nodeList:
            if node.learningRate != 0.0:
                allZero = False
        self.fixedLayer = not allZero


    # adds node to front of node list fully connected to previous layer
    def addNode(self, learningRate, activationFunction, inverseActivationFunction):
        # modify current layer
        newNode = Node(learningRate, activationFunction, inverseActivationFunction)
        self.nodeList.insert(0, newNode)
        self.weightList.insert(0, np.random.normal(0.0, pow(self.numInputNodes-1, -0.5), self.numInputNodes).tolist())
        self.numNodes += 1
        self.numNonBiasNodes += 1

        # modify next layer
        nextLayer = self.nextLayer
        nextLayer.numInputNodes += 1
        nextLayerWeightList = nextLayer.weightList
        for nodeWeights in nextLayerWeightList:
            nodeWeights.insert(0, np.random.normal(0.0, pow(nextLayer.numInputNodes-1, -0.5)))

    # calculate outputs based on inputs
    # inputs is a list of length numInputNodes
    # calculateOutputs will return the output WITHOUT the bias node
    def calculateOutputs(self, inputs):
        # error checking
        layer_bias_inputs = np.append(inputs, np.array(1.0))
        if len(layer_bias_inputs) != self.numInputNodes:
            print(len(layer_bias_inputs))
            print(self.numInputNodes)
            print("Wrong number of inputs; failed")
            exit(1)
        formattedInputs = np.array(layer_bias_inputs, ndmin=2).T
        layer_inputs = np.dot(self.weightList, formattedInputs)
        activationFunctions = []
        for node in self.nodeList:
            activationFunctions.append(node.activationFunction)
        layer_outputs = np.array([f(i) for f, i in zip(activationFunctions, layer_inputs)])
        return layer_outputs

    # updates learning rate of entire layer
    def updateLearningRatesLayer(self, newLearningRate):
        fNewLearningRate = float(newLearningRate)
        if fNewLearningRate == 0.0:
            self.fixedLayer = True
        else:
            self.fixedLayer = False
        for node in self.nodeList:
            node.updateLearningRate(fNewLearningRate)

# need to convert all weight and node lists to actual lists, not numpy ones
# this is because we need to add and delete nodes
class NeuralNetwork:
    # numNodes means how many nodes should be in that layer, not including bias nodes
    # position should be an int telling where to insert the new hidden layer, zero-indexed
    # 0 means right after the input layer, self.numHiddenLayers means right before the output layer
    def insertNewLayer(self, numNodes, position):
        if position < 0 or position > self.numHiddenLayers:
            print("Can't insert layer into that position")
            exit(1)
        defaultActivation = lambda x : scipy.special.expit(x)
        defaultInverseActivation = lambda x: scipy.special.logit(x)

        # fix self
        self.numHiddenLayers += 1

        # initialize new layer
        insertNodeList = []
        for index in range(numNodes):
            insertNodeList.append(Node(self.learningRate, defaultActivation, defaultInverseActivation))

        newLayer = HiddenLayer(numNodes, None, None, None, None, insertNodeList)
        # because input layer is the first input
        self.layerList.insert(position+1, newLayer)

        newLayer.prevLayer = self.layerList[position]
        newLayer.nextLayer = self.layerList[position+2]
        newLayer.numInputNodes = newLayer.prevLayer.numNodes
        newLayer.weightList = np.random.normal(0.0, pow(newLayer.numInputNodes-1, -0.5), (numNodes, newLayer.numInputNodes)).tolist()
        # newLayer.nodeList = insertNodeList

        # fix next and prev layers pointers
        newLayer.prevLayer.nextLayer = newLayer
        newLayer.nextLayer.prevLayer = newLayer

        # fix next layer weights
        newLayer.nextLayer.numInputNodes = newLayer.numNodes
        newLayer.nextLayer.weightList = np.random.normal(0.0, pow(newLayer.numNodes-1, -0.5), (newLayer.nextLayer.numNonBiasNodes, newLayer.numNodes)).tolist()

    # deletes the hidden layer as position, which is an int and zero-indexed
    # for example, deleteLayer(0) deletes the first hidden layer
    def deleteLayer(self, position):
        if self.numHiddenLayers == 0 or position < 0 or position >= self.numHiddenLayers:
            print("Tried to delete nonexistant layer")
            exit(1)
        # fixing the next and prev layer pointers
        prevLayer = self.layerList[position]
        nextLayer = self.layerList[position+2]
        prevLayer.nextLayer = nextLayer
        nextLayer.prevLayer = prevLayer

        # fixing the next layer weight and numInputs
        nextLayer.numInputNodes = prevLayer.numNodes
        nextLayer.weightList = np.random.normal(0.0, pow(nextLayer.numInputNodes-1, -0.5), (nextLayer.numNonBiasNodes, nextLayer.numInputNodes))

        # deleting layer
        del self.layerList[position+1]
        self.numHiddenLayers -= 1


    # hiddenLayerList is a list of ints which corresponds to how many nodes are in each hidden layer
    # numInputNodes is an int which says how many input nodes are expected
    # numOutputNodes is an int which says how many output nodes are expected
    # learningRate is the default learning rate for all non bias nodes
    def __init__(self, hiddenLayerList, numInputNodes, numOutputNodes, learningRate):
        defaultActivation = lambda x : scipy.special.expit(x)
        defaultInverseActivation = lambda x: scipy.special.logit(x)
        self.learningRate = learningRate

        # initialize input and output layers

        inputNodeList = []
        for index in range(numInputNodes):
            inputNodeList.append(Node(0.0, lambda x : x, lambda x : x))
        NNinputLayer = InputLayer(numInputNodes, None, inputNodeList)

        outputNodeList = []
        for index in range(numOutputNodes):
            outputNodeList.append(Node(learningRate, defaultActivation, defaultInverseActivation))

        outputWeightList = np.random.normal(0.0, pow(NNinputLayer.numNodes-1, -0.5), (numOutputNodes, NNinputLayer.numNodes))
        NNoutputLayer = OutputLayer(numOutputNodes, NNinputLayer, NNinputLayer.numNodes, outputNodeList, outputWeightList)
        NNinputLayer.nextLayer = NNoutputLayer

        self.layerList = [NNinputLayer, NNoutputLayer]
        self.numHiddenLayers = 0

        # add hidden layers

        for index in range(len(hiddenLayerList)):
            self.insertNewLayer(hiddenLayerList[index], index)

    # will only update with default learning rate
    # no need to add error bias and then get rid of it again in train
    def train(self, inputArray, targetList):
        targets = np.array(targetList, ndmin=2).T
        inputs = self.layerList[0].calculateOutputs(inputArray)
        errorList = []
        curOutput = inputs
        outputList = [curOutput]

        # output list is a list of all outputs, including the inputs
        # it doesn't count the output of the bias node
        for index in range(1, len(self.layerList)):
            curInput = curOutput
            curOutput = self.layerList[index].calculateOutputs(curInput)
            outputList.append(curOutput)
        finalOutput = outputList[-1]

        # outputListWithBias is a function which has all the outputs, including the
        # input. It also includes the bias node
        outputListWithBias = []

        for output in outputList[:-1]:
            outputListWithBias.append(np.append(output, np.array([[1.0]]), axis=0))
        outputListWithBias.append(finalOutput)

        # errorList is a list of errors, except the input layer
        # since the input layer obviously can't have errors
        # it DOES include the bias node
        # this is the derivative of the error function
        errorLast = targets - finalOutput
        sigDerivative = outputList[-1] * (1.0-outputList[-1])
        errorList = [errorLast * sigDerivative]

        for index in range(self.numHiddenLayers, 0, -1):
            curLayer = self.layerList[index+1]
            prevError = errorList[-1]
            if index != self.numHiddenLayers:
                prevError = prevError[:-1]
            sigDerivative = (outputList[index] * (1.0-outputList[index]))
            weightListMult = np.array(curLayer.weightList).T

            # print("prevError")
            # print(prevError)
            # print("outputlist[index]")
            # print(outputList[index])
            # print("sigDerivative")
            # print(sigDerivative)

            # print("weightListMult")
            # print(np.array(curLayer.weightList).T)

            prevErrorWeighted = np.dot(weightListMult, prevError)
            # print("prevErrorWeighted")
            # print(prevErrorWeighted)

            biasError = prevErrorWeighted[-1]

            nextUse = prevErrorWeighted[:-1]
            # print("nextUse")
            # print(nextUse)
            noBiasError = sigDerivative * nextUse
            # print ("noBiasError")
            # print(noBiasError)
            # print("appendMe")
            appendMe = np.append(noBiasError,[biasError],axis=0)
            # print(appendMe)


            errorList.append(appendMe)
            # print("")
            # print("")
        errorList.reverse()

        print("Error list")
        for item in errorList:
            print(item)
            print("")
        print("")
        print("")


        for index in range(0, self.numHiddenLayers+1):
            myError = errorList[index]
            if index != self.numHiddenLayers:
                myError = myError[:-1]
            #sigDerivative = (outputList[index+1]) * (1.0-outputList[index+1])
            #first = myError * sigDerivative
            first = myError
            correction = self.learningRate * np.dot(first, outputListWithBias[index].T)
            self.layerList[index+1].weightList = (self.layerList[index+1].weightList + correction).tolist()

    def query(self, inputArray):
        # probably can consolidate first calculateOutputs into for loop
        # print("inputArray")
        # print(inputArray)
        curOutput = self.layerList[0].calculateOutputs(inputArray)
        # print("curOutput original")
        # print(curOutput)
        outputList = [curOutput]

        for index in range(1, len(self.layerList)):
            # chance for optimization: we don't need to keep track of outputList here
            curInput = curOutput
            curOutput = self.layerList[index].calculateOutputs(curInput)
            outputList.append(curOutput)

            # print("curOutput in loop")
            # print(curOutput)

        finalOutput = outputList[-1]
        return finalOutput

