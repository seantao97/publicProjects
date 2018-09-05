# Some basic functions for neural networks to make programming easy.

import csv
import re
import operator
import time
import random
import numpy
import os
import scipy.io
from pprint import pprint
from random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.models import Model
from keras import backend as K
import h5py
import matplotlib.pyplot as plt
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets
import seaborn as sns
import pandas
from sklearn.preprocessing import LabelEncoder
import operator
from keras import regularizers


# collects like in 210 function
# input: a list of tuples
# output: dictionary of keys to lists of associated values, just like collect
def collect(tup):
    di = {}
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di

# How to get intermediate output stuff
# given curInput, model, get layerIndex outputs
# curInput can be a lot of inputs, in which case an array will be returned
# this gets the outputs of the first hidden layer
# print(bf.getIntermediateOutputs(model, 1, X))
def getIntermediateOutputs(model, layerIndex, curInput):
    intermediate_layer_model = Model(inputs=model.input,
                                     outputs=model.get_layer(index=layerIndex).output)
    return intermediate_layer_model.predict(curInput)

#
#
# ON A SIMILAR NOTE...
#
#
# Correct how to get first layer weights
# print("shape of first layer weights")
# print(model.layers[0].get_weights())

# data is an array of arrays, with each inner array representing one row of data
# num means is just how many means you want to use
# num init is how many times you want to init for the kmeans algorithm
def kmeans(data, numMeans, numInit):
    # k means in labels, sorted by X
    est = KMeans(n_clusters=numMeans, n_init=numInit, precompute_distances='auto')
    est.fit(data)
    labels = est.labels_
    return est, labels

# converts labels to colors
# labels is an array of ints (labels)
# colors is an array of strings representing colors
def convertLabelsToColors(labels, colors):
    colorLabels = []
    for label in labels:
        colorLabels.append(colors[int(label)])
    return colorLabels


# dataX, Y, and Z are just one dimensional arrays representing the x, y, and z coordinates
# the labels are just strings for the graphs
# title is just a string
# pathAndFileName is just a string
def create3DPlot(dataX, dataY, dataZ, xAxisLabel, yAxisLabel, zAxisLabel, title, pathAndFileName, figNum, colorArr):
    fignum = figNum
    fig = plt.figure(fignum, figsize=(4, 3))
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    ax.scatter(dataX, dataY, dataZ,
               c=colorArr, edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel(xAxisLabel)
    ax.set_ylabel(yAxisLabel)
    ax.set_zlabel(zAxisLabel)

    ax.set_title(title)
    ax.dist = 12
    fig.savefig(pathAndFileName)

# dataX, Y are just one dimensional arrays representing the x, y coordinates
# the labels are just strings for the graphs
# title is just a string
# pathAndFileName is just a string
def create2DPlot(dataX, dataY, xAxisLabel, yAxisLabel, title, pathAndFileName, figNum, colorArr):
    fig = plt.figure(figNum)
    ax = fig.add_subplot(111)
    ax.scatter(dataX, dataY, c=colorArr, edgecolor='k')
    ax.set_xlabel(xAxisLabel)
    ax.set_ylabel(yAxisLabel)
    ax.set_title(title)
    fig.savefig(pathAndFileName)

# X is the feature matrix (2D)
# X cannot be empty
# defaults to 0 if there is no variance
def spreadOut(X):
    if len(X) == 0 or len(X[0]) == 0:
        print("bad feature matrix")
        exit(0)
    max = []
    min = []
    for j in range(0, len(X[0])):
        max.append(X[0][j])
        min.append(X[0][j])
        for i in range(1, len(X)):
            if X[i][j] > max[j]:
                max[j] = X[i][j]
            if X[i][j] < min[j]:
                min[j] = X[i][j]
    for i in range(0, len(X)):
        for j in range(0, len(X[0])):
            if max[j] - min[j] != 0:
                X[i][j] = (X[i][j] - min[j]) / (max[j] - min[j])
            else:
                X[i][j] = 0


# gets the index of the 1 in a one hot arr
def maxIndexInOneHot(probArr):
    index, value = max(enumerate(probArr), key=operator.itemgetter(1))
    return index

# shuffles data and labels together
# each are arrays
def shuffleTogether(data, labels):
    a = np.array(data)
    b = np.array(labels)
    c = numpy.c_[a.reshape(len(a), -1), b.reshape(len(b), -1)]
    numpy.random.shuffle(c)
    a2 = c[:, :a.size // len(a)].reshape(a.shape)
    b2 = c[:, a.size // len(a):].reshape(b.shape)
    return a2, b2

# percent train is the percent which is the training set
# returns training set, validation set
# train is an array, percentTrain is just a number between 0 and 1
def split(train, percentTrain):
    splitPt = int(round(percentTrain * len(train)))
    return train[:splitPt], train[splitPt:]

#
#
# WARNING: THIS FUNCTION IS OUTDATED!!!!
#
#
# input is the normal 2D array
# output is a np array of one-hot of the correct category
# result eval function converts the output (one-hot) to index
def testNN(someModel, input, output, resultEvalFunction):
    numCorrect = 0.0
    numTotal = 0.0
    predictions = someModel.predict(input)
    for i, prediction in enumerate(predictions):
        res = resultEvalFunction(prediction)
        if res == maxIndexInOneHot(output[i]):
            numCorrect += 1.0
        numTotal += 1.0
    return numCorrect / numTotal

#
#
# WARNING: THIS FUNCTION IS REALLY SLOW, CAN JUST ADD PARAMETERS TO THE FIT FUNCTION
# WARNING: THIS FUNCTION IS OUTDATED, PLEASE USE SMARTTRAINNN
#
#
# trains a NN (someModel, a keras NN), on trainInput and trainOutput
# same code as testNN, except we don't run it on a test set
# I literally copied and pasted, and deleted the testing portion of the code
# takes one hot encoding for validation
# result eval function converts the output (basically probabilities of one-hot) to what output is compared to (index)
# path where to save temp checkpoints to
# maxBadCount is how many times you can go lower in accuracy between consectuive epochs before stopping training
def trainNN(someModel, trainInput, trainOutput, validationInput, validationOutput, resultEvalFunc, path, maxBadCount):
    validationAcc = 0.0
    lastValidationAcc = 0.0
    lastModel = someModel
    curModel = someModel
    numberEpochs = 0
    mostAccModel = someModel
    badCount = 0
    maxValidationPercent = 0.0


    # while validationAcc < 1.0 and numberEpochs < 10000 and badCount < maxBadCount:
    while numberEpochs < 10000 and badCount < maxBadCount:

        validationCorrect = 0
        validationTotal = 0

        lastModel = curModel
        lastValidationAcc = validationAcc

        if lastValidationAcc > maxValidationPercent:
            maxValidationPercent = lastValidationAcc
            model_json = lastModel.to_json()
            with open(path + "/model.json", "w") as json_file:
                json_file.write(model_json)
            lastModel.save_weights(path + "/modelWeights.h5")
            print("saving")

        curModel.fit(trainInput, trainOutput, epochs=1, batch_size=1)
        validationPrediction = curModel.predict(validationInput)
        validationResults = []
        for outputPrediction in validationPrediction:
            validationResults.append(resultEvalFunc(outputPrediction))
        # print("Validation prediction: ")
        # pprint(validationPrediction)
        # time.sleep(2)

        for i in range(0, len(validationResults)):
            if validationResults[i] == maxIndexInOneHot(validationOutput[i]):
                validationCorrect += 1
            validationTotal += 1

        # print("Validation results: ")
        # pprint(validationResults)
        # time.sleep(2)

        validationAcc = validationCorrect / validationTotal
        numberEpochs += 1
        print("Epoch: " + str(numberEpochs) + ", Validation acc: " + str(validationAcc))
        print("Correct: " + str(validationCorrect))
        print("Total: " + str(validationTotal))

        if validationAcc < lastValidationAcc:
            print("incrementing bad count: (" + str(badCount) + ")")
            badCount += 1


    with open(path + '/model.json', 'r') as json_file:
        mostAccModel = model_from_json(json_file.read())
    mostAccModel.load_weights(path + "/modelWeights.h5")

    mostAccModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return mostAccModel



#
# WARNING: THIS FUNCTION HAS NOT BEEN PROPERLY TESTED!!! (mostly the manual stuff)
#
# trains a NN (someModel, a keras NN), on trainInput and trainOutput
# same code as a bit smarter than trainNN, will have to be modified in the future
# takes one hot encoding for validation
# result eval function converts the output (basically probabilities of one-hot) to what output is compared to (index)
# path where to save temp checkpoints to
# maxBadCount is how many times you can go lower in accuracy between consectuive epochs before stopping training
# validationGraphPath is where the validation graph will go
# manualTuning is a bool saying whether input will be requested from the user for manual tuning
# minEpochs and maxEpochs are exactly what they say, but max is ignored if manualTuning is set to true
# manualGenerate is the condition which we wait for until we generate another user prompt, if manualTuning is set to true
#   is a string in the form of "[a-z]#", where
#   n denotes the number of epochs which must pass
#   b notes the number of badCounts
# figNum is as usual, an int describing the figure number
def smartTrainNN(someModel, trainInput, trainOutput, validationInput, validationOutput, resultEvalFunc, path, maxBadCount,
                 validationPathGraph, manualTuning, minEpochs, maxEpochs, manualGenerate, figNum):
    prevValidAccList = []
    epochNumList = []

    # manualTuning stuff
    userContinue = True
    n = 0
    whichCondition = ""
    b = 0
    if manualTuning:
        whichCondition = manualGenerate[0]
        if whichCondition == "n":
            n = int(manualGenerate[1:])
        elif whichCondition == "b":
            b = int(manualGenerate[1:])
        else:
            print("Bad input for manualGenerate, returning early")
            return
    else:
        userContinue = False

    validationAcc = 0.0
    lastValidationAcc = 0.0
    lastModel = someModel
    curModel = someModel
    numberEpochs = 0
    mostAccModel = someModel
    badCount = 0
    maxValidationPercent = 0.0

    lastBadCount = -1

    # while validationAcc < 1.0 and numberEpochs < 10000 and badCount < maxBadCount:
    while numberEpochs < minEpochs or userContinue or (not userContinue and numberEpochs < maxEpochs and badCount < maxBadCount):

        lastModel = curModel
        lastValidationAcc = validationAcc

        if lastValidationAcc >= maxValidationPercent:
            maxValidationPercent = lastValidationAcc
            model_json = lastModel.to_json()
            with open(path + "/model.json", "w") as json_file:
                json_file.write(model_json)
            lastModel.save_weights(path + "/modelWeights.h5")
            print("saving")

        hist = curModel.fit(trainInput, trainOutput, epochs=1, batch_size=1, validation_data=(validationInput, validationOutput))
        # validationPrediction = curModel.predict(validationInput)
        # validationResults = np.apply_along_axis(resultEvalFunc, 1, validationPrediction)
        #
        # for i in range(0, len(validationResults)):
        #     if validationResults[i] == maxIndexInOneHot(validationOutput[i]):
        #         validationCorrect += 1
        #     validationTotal += 1

        validationAcc = hist.history["val_acc"][0]
        numberEpochs += 1
        prevValidAccList.append(validationAcc)
        epochNumList.append(numberEpochs)
        print("Epoch: " + str(numberEpochs) + ", Validation acc: " + str(validationAcc))
        print("Correct: " + str(validationAcc * len(validationInput)))
        print("Total: " + str(len(validationInput)))

        if validationAcc < lastValidationAcc or 1.0 - validationAcc < 0.00001:
            print("incrementing bad count: (" + str(badCount) + ")")
            badCount += 1

        if userContinue and whichCondition == 'n' and numberEpochs >= minEpochs:
            if numberEpochs % n == 0:
                userResponse = input("Continue (number epochs passed)? y or Y to continue, anything else to quit")
                if userResponse != "y" and userResponse != "Y":
                    userContinue = False

        if userContinue and whichCondition == 'b' and numberEpochs >= minEpochs and badCount != lastBadCount:
            if badCount % b == 0:
                userResponse = input("Continue (bad count surpassed)? y or Y to continue, anything else to quit")
                if userResponse != "y" and userResponse != "Y":
                    userContinue = False
                else:
                    lastBadCount = badCount

        if 1.0 - validationAcc < 0.00001 and not userContinue:
            break



    with open(path + '/model.json', 'r') as json_file:
        mostAccModel = model_from_json(json_file.read())
    mostAccModel.load_weights(path + "/modelWeights.h5")

    mostAccModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    if validationPathGraph != "":
        colorArr = []
        for i in range(len(epochNumList)):
            colorArr.append("black")
        create2DPlot(epochNumList, prevValidAccList, "epochNumber", "validation acc", "Training info", validationPathGraph, figNum, colorArr)

    return mostAccModel