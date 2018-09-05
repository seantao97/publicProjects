from my_ANN_interface import *
import numpy as np
import scipy.special
import scipy.misc
import matplotlib.pyplot
import time

mnistDEEPANN = NeuralNetwork([100],784,10,0.1)
epochs = 1
training_data_file = open("mnist_train_full.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

test_data_file = open("mnist_test_full.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(",")
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = np.zeros(10) + 0.01
        targets[int(all_values[0])] = 0.99
        mnistDEEPANN.train(inputs, targets)

num_correct = 0.0
num_total = 0.0
for record in test_data_list:
    all_values = record.split(",")
    correct_label = int(all_values[0])
    # print(correct_label, "correct label")
    inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    outputs = mnistDEEPANN.query(inputs)
    label = np.argmax(outputs)
    # print(label, "network's answer")
    if(label == correct_label):
        num_correct += 1.0
    num_total += 1.0
print("percent correct:", num_correct/num_total)