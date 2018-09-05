from my_ANN_interface import *
import numpy as np
import scipy.special
import scipy.misc
import matplotlib.pyplot
import time


# https://theclevermachine.wordpress.com/2014/09/06/derivation-error-backpropagation-gradient-descent-for-neural-networks/
# https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/

# hiddenLayerList is a list of ints which corresponds to how many nodes are in each hidden layer
# numInputNodes is an int which says how many input nodes are expected
# numOutputNodes is an int which says how many output nodes are expected
# learningRate is the default learning rate for all non bias nodes
# def __init__(self, hiddenLayerList, numInputNodes, numOutputNodes, learningRate):

# This tests correctness of the ANN

# Code for printing out all of the info from the layers
# for index in range(1,len(myANN2.layerList)):
#     print("\nnew wl")
#     # print("numNodes")
#     # print(myANN2.layerList[index].numNodes)
#     # print("numNonBiasNodes")
#     # print(myANN2.layerList[index].numNonBiasNodes)
#     # print("numInputNodes")
#     # print(myANN2.layerList[index].numInputNodes)
#     # print(myANN2.layerList[index].weightList)


myANN2 = NeuralNetwork([3,2],2,2,15)


# Code for fixing layer weights
myANN2.layerList[1].weightList = [[0.1,0.2,0.3],[-0.1,-0.2,-0.3],[0.4,0.1,0.2]]
myANN2.layerList[2].weightList = [[0.1,0.2,0.3,0.4],[-0.1,-0.2,-0.3,-0.4]]
myANN2.layerList[3].weightList = [[0.1,0.2,0.3],[-0.1,-0.2,-0.3]]

print("query 6,1")
print(myANN2.query([6,1]))
print("query 4,2")
print(myANN2.query([4,2]))

for i in range(4):
    print("")


myANN2.train([4,2],[0,10])

# Code for printing out all of the info from the layers
print("After train [4,2] to [0,10]")
for index in range(1,len(myANN2.layerList)):
    print("\nnew wl")
    print("numNodes")
    print(myANN2.layerList[index].numNodes)
    print("numNonBiasNodes")
    print(myANN2.layerList[index].numNonBiasNodes)
    print("numInputNodes")
    print(myANN2.layerList[index].numInputNodes)
    print(myANN2.layerList[index].weightList)

for i in range(4):
    print("")

print("After training, query 3,5")
print(myANN2.query([3,5]))




# Code for querying and training
# print(myANN2.query([6,1]))
# myANN2.train([6,1],[1,0])
# print(myANN2.query([6,1]))


# Code for adding nodes, deleting nodes, adding layers, and deleting layers
# myANN2.layerList[1].deleteNode(1)
# myANN2.insertNewLayer(7,1)
# myANN2.layerList[3].addNode(0.499, lambda x : scipy.special.expit(x),lambda x: scipy.special.logit(x))
# myANN2.insertNewLayer(10,3)
# myANN2.deleteLayer(3)


# This tests a single layer ANN
#
# mnistDEEPANN = NeuralNetwork([100],784,10,0.1)
# epochs = 1
# training_data_file = open("mnist_train_full.csv", 'r')
# training_data_list = training_data_file.readlines()
# training_data_file.close()
#
# test_data_file = open("mnist_test_full.csv", 'r')
# test_data_list = test_data_file.readlines()
# test_data_file.close()
#
# for e in range(epochs):
#     for record in training_data_list:
#         all_values = record.split(",")
#         inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
#         targets = np.zeros(10) + 0.01
#         targets[int(all_values[0])] = 0.99
#         mnistDEEPANN.train(inputs, targets)
#
# num_correct = 0.0
# num_total = 0.0
# for record in test_data_list:
#     all_values = record.split(",")
#     correct_label = int(all_values[0])
#     # print(correct_label, "correct label")
#     inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
#     outputs = mnistDEEPANN.query(inputs)
#     label = np.argmax(outputs)
#     # print(label, "network's answer")
#     if(label == correct_label):
#         num_correct += 1.0
#     num_total += 1.0
# print("percent correct:", num_correct/num_total)

print("terminated")