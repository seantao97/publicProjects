'''
DEPRECATED!!!!!

Works on the world-famous iris dataset

Sample code to test some of the assumptions of the algorithm I invented...

Newer code which actually implements the algorithm is private, since I'm still
working on the finishing touches.

extremely accurate iris: https://groups.google.com/forum/#!topic/keras-users/Q2pSRCvTfSw
'''

import matplotlib
matplotlib.use('TkAgg')
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import regularizers
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
import numpy as np
import matplotlib.pyplot as plt
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets
import basicFunctions as bf
import seaborn as sns
import pandas
from sklearn.preprocessing import LabelEncoder
import operator
from keras.models import Model
from keras import backend as K
from sklearn.preprocessing import normalize

# red, green, blue, black, yellow, fushia (dark purple-ish), aqua (light blue), white, grey
nineColors = ["#ff0000","#00ff00","#0000ff","#000000","#ffff00", "#ff00ff", "#00ffff", "#ffffff", "#808080"]


def resultEvalFunc(probArr):
    index, value = max(enumerate(probArr), key=operator.itemgetter(1))
    return index

# testing code

# load dataset
dataframe = pandas.read_csv("/Users/seantao/Desktop/ml own stuff/datasets/iris.csv", header=None)
dataset = dataframe.values
X = dataset[:,0:4].astype(float)
# Y looks something like [iris-a, iris-b...etc.]
Y = dataset[:,4]

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
# encoded_Y looks something like [0,0,1,2...etc.]
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

dummy_y = np_utils.to_categorical(encoded_Y)

X, dummy_y = bf.shuffleTogether(X, dummy_y)

X = normalize(X)
bf.spreadOut(X)

# final output of iris
# X_train is [[num1, num2, num3, num4],...etc.]
# y_train is [[0,0,1],[0,1,0]...etc.]
X_train, X_nonTrain = bf.split(X, 0.7)
y_train, y_nonTrain = bf.split(dummy_y, 0.7)
X_validation, X_test = bf.split(X_nonTrain, 0.5)
y_validation, y_test = bf.split(y_nonTrain, 0.5)

est1, kMeans1 = bf.kmeans(X_train, 2, 30)
kMeans1Validation = est1.predict(X_validation)

kmeans1OneHot = np_utils.to_categorical(kMeans1)
kMeans1ValidationOneHot = np_utils.to_categorical(kMeans1Validation)

mean0X_train = []
mean0Y_train = []

mean1X_train = []
mean1Y_train = []

mean0X_validation = []
mean0Y_validation = []

mean1X_validation = []
mean1Y_validation = []

for index, mean in enumerate(kMeans1):
    if mean == 0:
        mean0X_train.append(X_train[index])
        mean0Y_train.append(y_train[index])
    else:
        mean1X_train.append(X_train[index])
        mean1Y_train.append(y_train[index])

for index, mean in enumerate(kMeans1Validation):
    if mean == 0:
        mean0X_validation.append(X_validation[index])
        mean0Y_validation.append(y_validation[index])
    else:
        mean1X_validation.append(X_validation[index])
        mean1Y_validation.append(y_validation[index])

mean0X_train = np.array(mean0X_train)
mean0Y_train = np.array(mean0Y_train)

mean1X_train = np.array(mean1X_train)
mean1Y_train = np.array(mean1Y_train)

mean0X_validation = np.array(mean0X_validation)
mean0Y_validation = np.array(mean0Y_validation)

mean1X_validation = np.array(mean1X_validation)
mean1Y_validation = np.array(mean1Y_validation)

# red is mean 0
# blue is mean 1
colorArr = bf.convertLabelsToColors(kMeans1, ["r", "b"])
bf.create3DPlot(X_train[:, 3], X_train[:, 0], X_train[:, 2], 'Petal width', 'Sepal length',
                'Petal length', "split all data k means", "/Users/seantao/Desktop/ml own stuff/plots/kMeans1.png",
                1, colorArr)

modelMeansSplit = Sequential()
modelMeansSplit.add(Dense(4, activation='tanh', input_dim=4, kernel_regularizer=regularizers.l1(0.005)))
modelMeansSplit.add(Dense(2, activation='softmax'))

modelMeansSplit.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeansSplit\n\n")
bf.trainNN(modelMeansSplit, X_train, kmeans1OneHot, X_validation, kMeans1ValidationOneHot, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 100)


modelMeans0 = Sequential()
modelMeans0.add(Dense(4, activation='tanh', input_dim=4, kernel_regularizer=regularizers.l2(0.001)))
modelMeans0.add(Dense(3, activation='softmax'))

modelMeans0.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeans0\n\n")
bf.trainNN(modelMeans0, mean0X_train, mean0Y_train, mean0X_validation, mean0Y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 100)


mean0X_predictions = modelMeans0.predict(mean0X_train)
mean0ColorLabelArr = []
for index in range(len(mean0X_predictions)):
    prediction = resultEvalFunc(mean0X_predictions[index])
    actual = resultEvalFunc(mean0Y_train[index])
    mean0ColorLabelArr.append(3 * actual + prediction)

mean0ColorArr = bf.convertLabelsToColors(mean0ColorLabelArr, nineColors)
bf.create3DPlot(mean0X_train[:, 3], mean0X_train[:, 0], mean0X_train[:, 2], 'Petal width', 'Sepal length',
                'Petal length', "mean0 neural net classification", "/Users/seantao/Desktop/ml own stuff/plots/mean0X.png",
                2, mean0ColorArr)

modelMeans1 = Sequential()
modelMeans1.add(Dense(4, activation='tanh', input_dim=4,  kernel_regularizer=regularizers.l2(0.001)))
modelMeans1.add(Dense(3, activation='softmax'))

modelMeans1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeans1\n\n")
bf.trainNN(modelMeans1, mean1X_train, mean1Y_train, mean1X_validation, mean1Y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 100)

mean1X_predictions = modelMeans1.predict(mean1X_train)
mean1ColorLabelArr = []
for index in range(len(mean1X_predictions)):
    prediction = resultEvalFunc(mean1X_predictions[index])
    actual = resultEvalFunc(mean1Y_train[index])
    mean1ColorLabelArr.append(3 * actual + prediction)
mean1ColorArr = bf.convertLabelsToColors(mean1ColorLabelArr, nineColors)


bf.create3DPlot(mean1X_train[:, 3], mean1X_train[:, 0], mean1X_train[:, 2], 'Petal width', 'Sepal length',
                'Petal length', "mean1 neural net classification", "/Users/seantao/Desktop/ml own stuff/plots/mean1X.png",
                3, mean1ColorLabelArr)

combineTrainInputArr = []
for index in range(len(X_train)):
    splitFeatures = bf.getIntermediateOutputs(modelMeansSplit, 1, np.array([X_train[index]]))
    mean0Features = bf.getIntermediateOutputs(modelMeans0, 1, np.array([X_train[index]]))
    mean1Features = bf.getIntermediateOutputs(modelMeans1, 1, np.array([X_train[index]]))
    cur = np.append(splitFeatures[0], mean0Features[0])
    cur = np.append(cur, mean1Features[0])
    combineTrainInputArr.append(cur)

combineTrainInputArr = np.array(combineTrainInputArr)

combineValidationInputArr = []
for index in range(len(X_validation)):
    splitFeatures = bf.getIntermediateOutputs(modelMeansSplit, 1, np.array([X_validation[index]]))
    mean0Features = bf.getIntermediateOutputs(modelMeans0, 1, np.array([X_validation[index]]))
    mean1Features = bf.getIntermediateOutputs(modelMeans1, 1, np.array([X_validation[index]]))
    cur = np.append(splitFeatures[0], mean0Features[0])
    cur = np.append(cur, mean1Features[0])
    combineValidationInputArr.append(cur)

combineValidationInputArr = np.array(combineValidationInputArr)

combineTestInputArr = []
for index in range(len(X_test)):
    splitFeatures = bf.getIntermediateOutputs(modelMeansSplit, 1, np.array([X_test[index]]))
    mean0Features = bf.getIntermediateOutputs(modelMeans0, 1, np.array([X_test[index]]))
    mean1Features = bf.getIntermediateOutputs(modelMeans1, 1, np.array([X_test[index]]))
    cur = np.append(splitFeatures[0], mean0Features[0])
    cur = np.append(cur, mean1Features[0])
    combineTestInputArr.append(cur)

combineTestInputArr = np.array(combineTestInputArr)

modelMeansCombine = Sequential()
modelMeansCombine.add(Dense(5, activation='tanh', input_dim=12,  kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine.add(Dense(3, activation='softmax'))

modelMeansCombine.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeansCombine\n\n")

bf.trainNN(modelMeansCombine, combineTrainInputArr, y_train, combineValidationInputArr, y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 150)

combinedColorLabelArray = []
trainPredictions = modelMeansCombine.predict(combineTrainInputArr)
for index in range(len(combineTrainInputArr)):
    prediction = resultEvalFunc(trainPredictions[index])
    actual = resultEvalFunc(y_train[index])
    combinedColorLabelArray.append(3 * actual + prediction)
combinedColorArr = bf.convertLabelsToColors(combinedColorLabelArray, nineColors)

bf.create3DPlot(X_train[:, 3], X_train[:, 0], X_train[:, 2], 'Petal width', 'Sepal length',
                'Petal length', "combined neural net classification", "/Users/seantao/Desktop/ml own stuff/plots/combinedOriginalInput.png",
                4, combinedColorArr)



print("\n\nmodelMeansSplit weights:")
print(modelMeansSplit.layers[0].get_weights())

print("\nmodelMeans0 weights:")
print(modelMeans0.layers[0].get_weights())

print("\nmodelMeans1 weights:")
print(modelMeans1.layers[0].get_weights())

print("\nmodelMeansCombine weights:")
print(modelMeansCombine.layers[0].get_weights())

print("\n\n")

print("\nMean 0 outputs: ")
print(mean0Y_train)
print("\nMean 0 validation outputs: ")
print(mean0Y_validation)
print("\nMean 0 predicitons: ")
print(mean0X_predictions)
print("\nColors: ")
print(mean0ColorArr)

print("\n\n")

print("\nMean 1 outputs: ")
print(mean1Y_train)
print("\nMean 1 validation outputs: ")
print(mean1Y_validation)
print("\nMean 1 predictions: ")
print(mean1X_predictions)
print("\nColors: ")
print(mean1ColorArr)

print("\n\nFinal accuracy")
print("\nTrain: ")
print(bf.testNN(modelMeansCombine, combineTrainInputArr, y_train, resultEvalFunc))
print("\nValidation: ")
print(bf.testNN(modelMeansCombine, combineValidationInputArr, y_validation, resultEvalFunc))
print("\nTest: ")
print(bf.testNN(modelMeansCombine, combineTestInputArr, y_test, resultEvalFunc))

# Shows the colors of the nine points
bf.create3DPlot([0,1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7,8], 'x', 'y',
                'z', "Graph of colors", "/Users/seantao/Desktop/ml own stuff/plots/colorGraph.png",
                5, nineColors)