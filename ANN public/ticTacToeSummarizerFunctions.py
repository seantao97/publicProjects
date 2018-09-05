'''
Some functions to help work with the tictactoe dataset from the UCI ML repo
'''

import numpy as np

import matplotlib
# matplotlib.use('TkAgg')
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten
# from keras import regularizers
# from keras.layers import Convolution2D, MaxPooling2D
# from keras.utils import np_utils
# import matplotlib.pyplot as plt
# # Though the following import is not directly being used, it is required
# # for 3D projection to work
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.cluster import KMeans
# from sklearn import datasets
# import basicFunctions as bf
# import seaborn as sns
# import pandas
# from sklearn.preprocessing import LabelEncoder
# import operator
# from keras.models import Model
# from keras import backend as K
# from sklearn.preprocessing import normalize
# from scipy.stats import ttest_ind
# import math
# import copy
# from sklearn.preprocessing import LabelEncoder
# from pprint import pprint
# import ast

# given a list of 9 0's, 1's and 2's, returns them as b's, o's, and x's
def boardStr(input):
    return np.array(eval(str(input).replace("0.0", '"b"').replace("1.0", '"o"').replace("2.0", '"x"')))

def boardStrFromArray(input):
    input.tolist()
    retList = []
    for i in range(9):
        if input[i] == 0:
            retList.append("b")
        elif input[i] == 1:
            retList.append("o")
        elif input[i] == 2:
            retList.append("x")
        else:
            exit(-1)
    return np.array(retList)

# given a list of 9 integers, prints them in a tic-tac-toe board style
def pboard(input):
    print(np.array(input).reshape((3,3)))

# given a list/tuple of boards, pretty prints them
# defaults to 3 boards since b, o, x
def pbox(input):
    for i in range(3):
        if i == 0:
            print("b")
        elif i == 1:
            print("o")
        else:
            print("x")
        pboard(input[i])
        print("\n")

# given a string representing an array of (tic-tac-toe boards, class_label, prevMean) (I think), prints the summary of the boards
def visualizerBoardLabelPrevMean(input):
    # 9 since there are 9 squares
    input = input.replace("array", "")
    # print(input)
    tupleList = eval(input)
    totalCounts = [np.zeros(9), np.zeros(9), np.zeros(9)] # b, o, x
    totalResults = [0, 0] # not win for x, win for x
    prevMeanResults = []
    prevMeanCounts = []
    prevMeanBoards = []
    for i in range(10):
        prevMeanCounts.append((np.zeros(9), np.zeros(9), np.zeros(9))) # b, o, x for that mean
        prevMeanResults.append([0,0])
        prevMeanBoards.append([])
    print("Length: " + str(len(tupleList)) + "\n\n")
    for tuple in tupleList:
        board = tuple[0]

        # print(board)
        # boardPrint = np.array(eval(str(board).replace("0.0", '"b"').replace("1.0", '"o"').replace("2.0", '"x"'))).reshape((3,3))
        # print(boardPrint)
        # exit(0)

        category = tuple[1]
        prevMean = tuple[2]
        totalResults[category] += 1
        prevMeanResults[prevMean][category] += 1
        prevMeanBoards[prevMean].append(boardStr(board))

        for i in range(9):
            val = board[i]
            totalCounts[int(val)][i] += 1
            prevMeanCounts[prevMean][int(val)][i] += 1
    print("Totals:\n")
    print(totalResults)
    pbox(totalCounts)
    print("\n\n")
    print("\n\n\n\n\nEnd 1\n\n\n\n\n")
    for i in range(len(prevMeanCounts)):
        print("\n")
        print("Prev mean " + str(i) + " numbers:")
        print(prevMeanResults[i])
    print("\n\n\n\n\nEnd 2\n\n\n\n\n")
    for i in range(len(prevMeanCounts)):
        print("\n")
        print("Prev mean " + str(i) + " summary:")
        print(prevMeanResults[i])
        print("\n")
        pbox(prevMeanCounts[i])
    print("\n\n\n\n\nEnd 3\n\n\n\n\n")

    for i in range(len(prevMeanBoards)):
        print("\n\nPrevMeanBoards" + str(i) + "\n\n")
        print(prevMeanResults[i])
        print("\n")
        pbox(prevMeanCounts[i])
        for boxStr in prevMeanBoards[i]:
            print(boxStr.reshape((3,3)))
            print("\n")
        print("\n")


# given a string representing an array of (tic-tac-toe boards, class_label), prints the summary of the boards
def visualizerBoardLabel(input):
    # 9 since there are 9 squares
    input = input.replace("array", "")
    # print(input)
    tupleList = eval(input)
    totalCounts = [np.zeros(9), np.zeros(9), np.zeros(9)]  # b, o, x
    totalResults = [0, 0]  # not win for x, win for x
    totalBoards = []
    print("Length: " + str(len(tupleList)) + "\n\n")
    for tuple in tupleList:
        board = tuple[0]
        totalBoards.append(board)

        category = tuple[1]
        totalResults[category] += 1

        for i in range(9):
            val = board[i]
            totalCounts[int(val)][i] += 1
    print("Totals:\n")
    print(totalResults)
    pbox(totalCounts)
    print("\n\n")
    print("\n\n\n\n\nEnd 1\n\n\n\n\n")

    for someBoard in totalBoards:
        pboard(boardStr(someBoard))
        print("\n")

    print("\n\n\n\n\nEnd 2\n\n\n\n\n")