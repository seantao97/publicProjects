'''


# Notes:

Works on the bank dataset from the UCI ML repository

Deprecated for similar reasons to the iris dataset...the actual code is in a private repo!

l2 in NN with individual means since we want to get high accuracy (overfit to outliers is fine)
l1 in NN which separates and combines (since we want to find features, overfit to outliers is not fine)
can do some simple test runs to find optimal coefficients for regularization, dropout,...etc.

   The zip file includes two datasets:
      1) bank-additional-full.csv with all examples, ordered by date (from May 2008 to November 2010).
      2) bank-additional.csv with 10% of the examples (4119), randomly selected from bank-additional-full.csv.
   The smallest dataset is provided to test more computationally demanding machine learning algorithms (e.g., SVM).

   The binary classification goal is to predict if the client will subscribe a bank term deposit (variable y).

5. Number of Instances: 41188 for bank-additional-full.csv

6. Number of Attributes: 20 + output attribute.

7. Attribute information:

   For more information, read [Moro et al., 2014].

   Input variables:
   # bank client data:
   1 - age (numeric)
   2 - job : type of job (categorical: "admin.","blue-collar","entrepreneur","housemaid","management","retired","self-employed","services","student","technician","unemployed","unknown")
   3 - marital : marital status (categorical: "divorced","married","single","unknown"; note: "divorced" means divorced or widowed)
   4 - education (categorical: "basic.4y","basic.6y","basic.9y","high.school","illiterate","professional.course","university.degree","unknown")
   5 - default: has credit in default? (categorical: "no","yes","unknown")
   6 - housing: has housing loan? (categorical: "no","yes","unknown")
   7 - loan: has personal loan? (categorical: "no","yes","unknown")
   # related with the last contact of the current campaign:
   8 - contact: contact communication type (categorical: "cellular","telephone")
   9 - month: last contact month of year (categorical: "jan", "feb", "mar", ..., "nov", "dec")
  10 - day_of_week: last contact day of the week (categorical: "mon","tue","wed","thu","fri")
  11 - duration: last contact duration, in seconds (numeric). Important note:  this attribute highly affects the output target (e.g., if duration=0 then y="no"). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.
   # other attributes:
  12 - campaign: number of contacts performed during this campaign and for this client (numeric, includes last contact)
  13 - pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)
  14 - previous: number of contacts performed before this campaign and for this client (numeric)
  15 - poutcome: outcome of the previous marketing campaign (categorical: "failure","nonexistent","success")
   # social and economic context attributes
  16 - emp.var.rate: employment variation rate - quarterly indicator (numeric)
  17 - cons.price.idx: consumer price index - monthly indicator (numeric)
  18 - cons.conf.idx: consumer confidence index - monthly indicator (numeric)
  19 - euribor3m: euribor 3 month rate - daily indicator (numeric)
  20 - nr.employed: number of employees - quarterly indicator (numeric)

  Output variable (desired target):
  21 - y - has the client subscribed a term deposit? (binary: "yes","no")


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

# figNum
globalFigNum = 1

# load dataset
dataframe = pandas.read_csv("/Users/seantao/Desktop/ml own stuff/bank_top_level/bank-additional/bank-additional-full.csv", sep=';')
dataset = dataframe.values


X1 = dataset[:,0].astype(float)
X11 = dataset[:,10].astype(float)
X12 = dataset[:,11].astype(float)
X13 = dataset[:,12].astype(float)
X14 = dataset[:,13].astype(float)
X16 = dataset[:,15].astype(float)
X17 = dataset[:,16].astype(float)
X18 = dataset[:,17].astype(float)
X19 = dataset[:,18].astype(float)
X20 = dataset[:,19].astype(float)

# now all the categoricals
encoder = LabelEncoder()

X2 = dataset[:,1]
encoder.fit(X2)
X2 = encoder.transform(X2)

X3 = dataset[:,2]
encoder.fit(X3)
X3 = encoder.transform(X3)

X4 = dataset[:,3]
encoder.fit(X4)
X4 = encoder.transform(X4)

X5 = dataset[:,4]
encoder.fit(X5)
X5 = encoder.transform(X5)

X6 = dataset[:,5]
encoder.fit(X6)
X6 = encoder.transform(X6)

X7 = dataset[:,6]
encoder.fit(X7)
X7 = encoder.transform(X7)

X8 = dataset[:,7]
encoder.fit(X8)
X8 = encoder.transform(X8)

X9 = dataset[:,8]
encoder.fit(X9)
X9 = encoder.transform(X9)

X10 = dataset[:,9]
encoder.fit(X10)
X10 = encoder.transform(X10)

X15 = dataset[:,14]
encoder.fit(X15)
X15 = encoder.transform(X15)

X = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,X12,X13,X14,X15,X16,X17,X18,X19,X20)).reshape(20,41188).T.astype(float)
Y = dataset[:,20]


encoder.fit(Y)
# encoded_Y looks something like [0,0,1,2...etc.]
encoded_Y = encoder.transform(Y)
dummy_y = np_utils.to_categorical(encoded_Y)

X, dummy_y = bf.shuffleTogether(X, dummy_y)

# Don't need to normalize I think
# X = normalize(X)
bf.spreadOut(X)

# final output of bank
# X_train is [[num1, num2, num3, num4],...etc.]
# y_train is [[0,0,1],[0,1,0]...etc.]
X_train, X_nonTrain = bf.split(X, 0.8)
y_train, y_nonTrain = bf.split(dummy_y, 0.8)
X_validation, X_test = bf.split(X_nonTrain, 0.5)
y_validation, y_test = bf.split(y_nonTrain, 0.5)

est1, kMeans1 = bf.kmeans(X_train, 3, 50)
kMeans1Validation = est1.predict(X_validation)

kmeans1OneHot = np_utils.to_categorical(kMeans1)
kMeans1ValidationOneHot = np_utils.to_categorical(kMeans1Validation)

mean0X_train = []
mean0Y_train = []

mean1X_train = []
mean1Y_train = []

mean2X_train = []
mean2Y_train = []

mean0X_validation = []
mean0Y_validation = []

mean1X_validation = []
mean1Y_validation = []

mean2X_validation = []
mean2Y_validation = []

for index, mean in enumerate(kMeans1):
    if mean == 0:
        mean0X_train.append(X_train[index])
        mean0Y_train.append(y_train[index])
    elif mean == 1:
        mean1X_train.append(X_train[index])
        mean1Y_train.append(y_train[index])
    else:
        mean2X_train.append(X_train[index])
        mean2Y_train.append(y_train[index])

for index, mean in enumerate(kMeans1Validation):
    if mean == 0:
        mean0X_validation.append(X_validation[index])
        mean0Y_validation.append(y_validation[index])
    elif mean == 1:
        mean1X_validation.append(X_validation[index])
        mean1Y_validation.append(y_validation[index])
    else:
        mean2X_validation.append(X_validation[index])
        mean2Y_validation.append(y_validation[index])

mean0X_train = np.array(mean0X_train)
mean0Y_train = np.array(mean0Y_train)

mean1X_train = np.array(mean1X_train)
mean1Y_train = np.array(mean1Y_train)

mean2X_train = np.array(mean2X_train)
mean2Y_train = np.array(mean2Y_train)

mean0X_validation = np.array(mean0X_validation)
mean0Y_validation = np.array(mean0Y_validation)

mean1X_validation = np.array(mean1X_validation)
mean1Y_validation = np.array(mean1Y_validation)

mean2X_validation = np.array(mean2X_validation)
mean2Y_validation = np.array(mean2Y_validation)

# red is mean 0
# blue is mean 1
# green is mean 2
colorArr = bf.convertLabelsToColors(kMeans1, ["r", "b", "g"])
# get rid of the y col since that's a y value
colNames = dataframe.columns.values[:-1]

# Should work but takes forever
# for i in range(len(colNames)):
#     for j in range(len(colNames)):
#         if i == j:
#             continue
#         else:
#             name = "Plot of " + colNames[j] + " vs " + colNames[i]
#             bf.create2DPlot(X_train[:, i], X_train[:, j], colNames[i], colNames[j], name,
#             "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/mean split 1 plots/" + name + ".png",
#                             globalFigNum, colorArr)
#             globalFigNum += 1
#             plt.close('all')


modelMeansSplitIter1 = Sequential()
modelMeansSplitIter1.add(Dense(40, activation='tanh', input_dim=20, kernel_regularizer=regularizers.l1(0.005)))
modelMeansSplitIter1.add(Dense(3, activation='softmax'))

modelMeansSplitIter1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeansSplit1\n\n")

bf.smartTrainNN(modelMeansSplitIter1, X_train, kmeans1OneHot, X_validation, kMeans1ValidationOneHot, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 3,
                "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/validation Acc graphs/modelMeansSplit1Iter1Validation.png",
                False, 1, 10, "", globalFigNum)
globalFigNum += 1
plt.close("all")


modelMeans0Iter1 = Sequential()
modelMeans0Iter1.add(Dense(50, activation='tanh', input_dim=20,  kernel_regularizer=regularizers.l2(0.001)))
modelMeans0Iter1.add(Dense(40, activation='tanh',  kernel_regularizer=regularizers.l2(0.001)))
modelMeans0Iter1.add(Dense(2, activation='softmax'))

modelMeans0Iter1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeans0Iter1\n\n")

bf.smartTrainNN(modelMeans0Iter1, mean0X_train, mean0Y_train, mean0X_validation, mean0Y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 3,
                "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/validation Acc graphs/modelMeans0Iter1Validation.png",
                False, 1, 10, "", globalFigNum)
globalFigNum += 1
plt.close("all")

# maybe do something with this later
mean0X_predictions = modelMeans0Iter1.predict(mean0X_train)

modelMeans1Iter1 = Sequential()
modelMeans1Iter1.add(Dense(50, activation='tanh', input_dim=20,  kernel_regularizer=regularizers.l2(0.001)))
modelMeans1Iter1.add(Dense(40, activation='tanh',  kernel_regularizer=regularizers.l2(0.001)))
modelMeans1Iter1.add(Dense(2, activation='softmax'))

modelMeans1Iter1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeans1Iter1\n\n")

bf.smartTrainNN(modelMeans1Iter1, mean1X_train, mean1Y_train, mean1X_validation, mean1Y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 3,
                "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/validation Acc graphs/modelMeans1Iter1Validation.png",
                False, 1, 10, "", globalFigNum)
globalFigNum += 1
plt.close("all")

# maybe do something with this later
mean1X_predictions = modelMeans1Iter1.predict(mean1X_train)

modelMeans2Iter1 = Sequential()
modelMeans2Iter1.add(Dense(50, activation='tanh', input_dim=20,  kernel_regularizer=regularizers.l2(0.001)))
modelMeans2Iter1.add(Dense(40, activation='tanh',  kernel_regularizer=regularizers.l2(0.001)))
modelMeans2Iter1.add(Dense(2, activation='softmax'))

modelMeans2Iter1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeans2Iter1\n\n")

bf.smartTrainNN(modelMeans2Iter1, mean2X_train, mean2Y_train, mean2X_validation, mean2Y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 3,
                "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/validation Acc graphs/modelMeans2Iter1Validation.png",
                False, 1, 10, "", globalFigNum)
globalFigNum += 1
plt.close("all")

# maybe do something with this later
mean2X_predictions = modelMeans2Iter1.predict(mean2X_train)

splitFeatures = bf.getIntermediateOutputs(modelMeansSplitIter1, 1, X_train)
mean0Features = bf.getIntermediateOutputs(modelMeans0Iter1, 2, X_train)
mean1Features = bf.getIntermediateOutputs(modelMeans1Iter1, 2, X_train)
mean2Features = bf.getIntermediateOutputs(modelMeans2Iter1, 2, X_train)

combineTrainInputArr = np.concatenate((splitFeatures, mean0Features, mean1Features, mean2Features), axis=1)


splitFeatures = bf.getIntermediateOutputs(modelMeansSplitIter1, 1, X_validation)
mean0Features = bf.getIntermediateOutputs(modelMeans0Iter1, 2, X_validation)
mean1Features = bf.getIntermediateOutputs(modelMeans1Iter1, 2, X_validation)
mean2Features = bf.getIntermediateOutputs(modelMeans2Iter1, 2, X_validation)

combineValidationInputArr = np.concatenate((splitFeatures, mean0Features, mean1Features, mean2Features), axis=1)

splitFeatures = bf.getIntermediateOutputs(modelMeansSplitIter1, 1, X_test)
mean0Features = bf.getIntermediateOutputs(modelMeans0Iter1, 2, X_test)
mean1Features = bf.getIntermediateOutputs(modelMeans1Iter1, 2, X_test)
mean2Features = bf.getIntermediateOutputs(modelMeans2Iter1, 2, X_test)

combineTestInputArr = np.concatenate((splitFeatures, mean0Features, mean1Features, mean2Features), axis=1)

modelMeansCombine1 = Sequential()
modelMeansCombine1.add(Dense(80, activation='tanh', input_dim=160,  kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(60, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(40, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(40, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(30, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(30, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(30, activation='tanh', kernel_regularizer=regularizers.l1(0.005)))
modelMeansCombine1.add(Dense(2, activation='softmax'))

modelMeansCombine1.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("\n\nTraining modelMeansCombine\n\n")

bf.smartTrainNN(modelMeansCombine1, combineTrainInputArr, y_train, combineValidationInputArr, y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 3,
                "/Users/seantao/Desktop/ml own stuff/bank_top_level/plots/validation Acc graphs/modelMeansCombine1Validation.png",
                False, 1, 10, "", globalFigNum)
globalFigNum += 1
plt.close("all")

bf.trainNN(modelMeansCombine, combineTrainInputArr, y_train, combineValidationInputArr, y_validation, resultEvalFunc,
           "/Users/seantao/Desktop/ml own stuff/graphs", 150)


# also probably create a plot based on the stuff we've found


# print("\n\nmodelMeansSplit weights:")
# print(modelMeansSplit.layers[0].get_weights())
#
# print("\nmodelMeans0 weights:")
# print(modelMeans0.layers[0].get_weights())
#
# print("\nmodelMeans1 weights:")
# print(modelMeans1.layers[0].get_weights())
#
# print("\nmodelMeansCombine weights:")
# print(modelMeansCombine.layers[0].get_weights())

# print("\n\n")
#
# print("\nMean 0 outputs: ")
# print(mean0Y_train)
# print("\nMean 0 validation outputs: ")
# print(mean0Y_validation)
# print("\nMean 0 predicitons: ")
# print(mean0X_predictions)
# print("\nColors: ")
# print(mean0ColorArr)
#
# print("\n\n")
#
# print("\nMean 1 outputs: ")
# print(mean1Y_train)
# print("\nMean 1 validation outputs: ")
# print(mean1Y_validation)
# print("\nMean 1 predictions: ")
# print(mean1X_predictions)
# print("\nColors: ")
# print(mean1ColorArr)

print("\n\nFinal accuracy")
print("\nTrain: ")
print(bf.testNN(modelMeansCombine, combineTrainInputArr, y_train, resultEvalFunc))
print("\nValidation: ")
print(bf.testNN(modelMeansCombine, combineValidationInputArr, y_validation, resultEvalFunc))
print("\nTest: ")
print(bf.testNN(modelMeansCombine, combineTestInputArr, y_test, resultEvalFunc))


