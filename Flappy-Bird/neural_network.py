import numpy as np

class NeuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        # initialize the number of nodes in each layer
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # generate weight and bias matrices using random function
        self.weights_IH = 2.5 * np.random.rand(self.hidden_nodes, self.input_nodes) - 1.25
        self.weights_HO = 2.5 * np.random.rand(self.output_nodes, self.hidden_nodes) - 1.25

        self.bias_H = 2.5 * np.random.rand(self.hidden_nodes, 1) - 1.25
        self.bias_O = 2.5 * np.random.rand(self.output_nodes, 1) - 1.25

        self.learning_rate = 0.02


    def get_hidden_weights_and_bias(self):
        return self.weights_IH, self.bias_H

    def get_output_weights_and_bias(self):
        return self.weights_HO, self.bias_O

    def set_hidden_weights_and_bias(self, hidden_weights, hidden_bias):
        self.weights_IH = hidden_weights
        self.bias_H = hidden_bias

    def set_output_weights_and_bias(self, output_weights, output_bias):
        self.weights_HO = output_weights
        self.bias_O = output_bias

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


    def derivative_siggmoid(self, x):
        # return self.sigmoid(x) * (1 - self.sigmoid(x)) # this is the original formula
        return x * (1 - x)


    def predict(self,input_list):
        # Convert the input list to a 2x1 numpy array/matrix
        input_matrix = np.reshape(np.array(input_list, dtype='float'),(-1,1))

        # Generating the hidden outputs
        hidden_matrix = np.matmul(self.weights_IH, input_matrix) + self.bias_H

        # Activation function i.e. sigmoid function in this case
        hidden_matrix = self.sigmoid(hidden_matrix)

        # Generate the output
        output_matrix = np.matmul(self.weights_HO, hidden_matrix)+ self.bias_O
        #Activation function
        output_matrix = self.sigmoid(output_matrix)
        return hidden_matrix, output_matrix


    def train(self, input_list, target_list):

        # get output from the feedforward NN
        hidden_matrix, outputs_matrix = self.predict(input_list)

        # convert list to numpy array
        input_matrix = np.reshape(np.array(input_list, dtype="float"),(-1,1))
        targets = np.reshape(np.array(target_list, dtype="float"),(-1,1))

        #calculate the error
        output_error = targets - outputs_matrix

        #calculate output gradients
        outputs_gradients = self.derivative_siggmoid(outputs_matrix) * output_error * self.learning_rate

        # Calculate the hidden->output deltas
        delta_weights_HO = np.matmul(outputs_gradients, hidden_matrix.transpose())

        # Adjust the output weights by delta # Adding delta to original weights
        self.weights_HO = self.weights_HO + delta_weights_HO

        # Adjust the output bias by delta
        self.bias_O = self.bias_O + outputs_gradients

        #calculate the hidden layer errors
        hidden_errors = np.matmul( self.weights_HO.transpose(), outputs_gradients)

        #calculate hidden gradients
        hidden_gradients = self.derivative_siggmoid(hidden_matrix) * hidden_errors * self.learning_rate

        #calculate the input -> hidden deltas
        delta_weights_IH = np.matmul(hidden_gradients, input_matrix.transpose())

        # Adjust the hidden weights by delta
        self.weights_IH = self.weights_IH + delta_weights_IH

        # Adjust the hidden bias by delta
        self.bias_H = self.bias_H + hidden_gradients
