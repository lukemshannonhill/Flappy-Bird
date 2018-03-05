import numpy as np

class NeuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        # initialize the number of nodes in each layer
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # generate weight and bias matrices using random function
        self.weights_IH = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.weights_HO = np.random.rand(self.output_nodes, self.hidden_nodes)

        self.bias_H = np.random.rand(self.hidden_nodes, 1)
        self.bias_O = np.random.rand(self.output_nodes, 1)


        self.learning_rate = 0.2;


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


    def derivative_siggmoid(self, x):
        # return self.sigmoid(x) * (1 - self.sigmoid(x)) # this is the original formula
        return x * (1 - x)


    def feedforward(self,input_list):
        # Convert the input list to a 2x1 numpy array/matrix
        input_matrix = np.reshape(np.array(input_list),(-1,1))

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
        hidden_matrix, outputs_matrix = self.feedforward(input_list)

        # convert list to numpy array
        input_matrix = np.reshape(np.array(input_list),(-1,1))
        targets = np.array(target_list)

        #calculate the error
        output_error = targets - outputs_matrix
        # print(targets,"-",str(outputs_matrix),"=",output_error)

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
        self.bias_H = self.bias_H + outputs_gradients
