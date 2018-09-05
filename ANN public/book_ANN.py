import numpy as np
import scipy.special
import scipy.misc
import matplotlib.pyplot
import time


# neural netwrok class definition
class neuralNetwork:

    # initialize neutal network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.lr = learningrate

        # link weights matricies
        # probably should make sure they aren't zero??
        # shouldn't we pow by self.inodes and self.hnodes, respectively??
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))


        self.activation_function = lambda x : scipy.special.expit(x)
        self.inverse_activation_function = lambda x: scipy.special.logit(x)




    # train neural network
    def train(self, inputs_list, targets_list):
        # converts inputs list to 2 array (vertical of 784)
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        # calculates signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # calcuates signals emerging from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # calculates signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculates signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        # output layer error is target-actual
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)
        # update the weights for the links between the hidden and output layers
        self.who += self.lr * (np.dot((output_errors * final_outputs * (1.0-final_outputs)), np.transpose(hidden_outputs)))
        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0-hidden_outputs)), np.transpose(inputs))

    def query(self, inputs_list):
        # converts input list to 2d array (vertical of 784)
        inputs = np.array(inputs_list, ndmin=2).T
        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # calculate signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # calcuate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculate the signals emerging from the final output
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

    # backquery the neural network
    # we'll use the same terminmology to each item,
    # eg target are the values at the right of the network, albeit used as input
    # eg hidden_output is the signal to the right of the middle nodes
    def backquery(self, targets_list):
        # transpose the targets list to a vertical array
        final_outputs = np.array(targets_list, ndmin=2).T

        # calculate the signal into the final output layer
        final_inputs = self.inverse_activation_function(final_outputs)

        # calculate the signal out of the hidden layer
        hidden_outputs = np.dot(self.who.T, final_inputs)
        # scale them back to 0.01 to .99
        hidden_outputs -= np.min(hidden_outputs)
        hidden_outputs /= np.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01

        # calculate the signal into the hideen layer
        hidden_inputs = self.inverse_activation_function(hidden_outputs)

        # calculate the signal out of the input layer
        inputs = np.dot(self.wih.T, hidden_inputs)
        # scale them back to 0.01 to .99
        inputs -= np.min(inputs)
        inputs /= np.max(inputs)
        inputs *= 0.98
        inputs += 0.01

        return inputs

##
##
## Trial Code
##
##

# myList = np.random.normal(0.0, 1.0, (2, 3))
# for thing in myList:
#     print (thing)
#
# longList = [1,2,3,4,5,6,7,8,9,10,11,12]
# twod = np.array(longList, ndmin=2).T
# for row in twod:
#     print(row)
# small_test = open("mnist_train_100.csv", 'r')
# for line in small_test.readlines():
#     vals = line.split(",")
#     print(len(vals))
# first_image = small_test.readline().split(',')
# image_array = np.asfarray(first_image[1:]).reshape((28,28))
# matplotlib.pyplot.imshow(image_array, cmap='Greys', interpolation='None')
# matplotlib.pyplot.savefig("trial_plot.jpeg")

# rotate image:

# small_test.close()

##
##
## Initialization and Training
##
##

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.1
epochs = 1
n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
training_data_file = open("mnist_train_full.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(",")
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = np.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)

test_data_file = open("mnist_test_full.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

##
##
## Testing
##
##

num_correct = 0.0
num_total = 0.0
for record in test_data_list:
    all_values = record.split(",")
    correct_label = int(all_values[0])
    # print(correct_label, "correct label")
    inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    outputs = n.query(inputs)
    label = np.argmax(outputs)
    # print(label, "network's answer")
    if(label == correct_label):
        num_correct += 1.0
    num_total += 1.0
print("percent correct:", num_correct/num_total)

# for index in range(output_nodes):
#     # create the output signals for this label
#     targets = np.zeros(output_nodes) + 0.01
#     # all_values[0] is the target label for this record
#     targets[index] = 0.99
#     # get image data
#     image_data = n.backquery(targets)
#     # filename
#     filename = "backquery" + str(index) + ".jpeg"
#     # plot image data
#     matplotlib.pyplot.imshow(image_data.reshape(28, 28), cmap='Greys', interpolation='None')
#     matplotlib.pyplot.savefig(filename)







