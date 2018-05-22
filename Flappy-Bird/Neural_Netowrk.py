import numpy as np


class NeuronLayer:
    def __init__(self, neurons, neurons_in_previous_layer, b=[0.0], w=[[0.0]]):
        # import time
        # np.random.seed(int(time.time()))
        # np.random.seed(1)
        self.bias = np.random.random()
        self.weights_from_previous_to_this = 2 * np.random.random((neurons_in_previous_layer, neurons)) - self.bias

        # self.bias = b
        # self.weights_from_previous_to_this = w
        # print("bias", self.bias)
        # print("weights", self.weights_from_previous_to_this)
        # print("----")
        # self.weights_from_previous_to_this = 2 * np.random.random((neurons_in_previous_layer, neurons)) - 1


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.hidden_layer = NeuronLayer(hidden_nodes, input_nodes, b=[0.8990440160748187],
                                        w=[[-0.05353412, 0.6649129, -0.24340758, -0.0416839],
                                           [-0.55266982, -0.50163635, 0.28309926, -0.07587811]])
        self.output_layer = NeuronLayer(output_nodes, hidden_nodes, b=[0.23084011213966216], w=[[1.58517134],
                                                                                                [0.25307128],
                                                                                                [1.08582508],
                                                                                                [1.10956104]])

    def get_hidden_weights_and_bias(self):
        return self.hidden_layer.weights_from_previous_to_this, self.hidden_layer.bias

    def get_output_weights_and_bias(self):
        return self.output_layer.weights_from_previous_to_this, self.output_layer.bias

    def set_hidden_weights_and_bias(self, hidden_weights, hidden_bias):
        self.hidden_layer.weights_from_previous_to_this = hidden_weights
        self.hidden_layer.bias = hidden_bias

    def set_output_weights_and_bias(self, output_weights, output_bias):
        self.output_layer.weights_from_previous_to_this = output_weights
        self.output_layer.bias = output_bias

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            output_from_layer_1, output_from_layer_2 = self.predict(training_set_inputs)
            output_error = training_set_outputs - output_from_layer_2
            output_gradient = output_error * self.sigmoid_derivative(output_from_layer_2)
            hidden_error = np.dot(output_gradient, self.output_layer.weights_from_previous_to_this.T)
            hidden_gradient = hidden_error * self.sigmoid_derivative(output_from_layer_1)

            hidden_adjustment = np.dot(training_set_inputs.T, hidden_gradient)
            output_adjustment = np.dot(output_from_layer_1.T, output_gradient)

            self.hidden_layer.weights_from_previous_to_this += hidden_adjustment
            self.output_layer.weights_from_previous_to_this += output_adjustment

            self.hidden_layer.bias = self.hidden_layer.bias + hidden_gradient
            self.output_layer.bias = self.output_layer.bias + output_gradient

    def predict(self, inputs, test=False):
        hidden_output = self.sigmoid(
            np.dot(inputs, self.hidden_layer.weights_from_previous_to_this)
        )
        output = self.sigmoid(
            np.dot(hidden_output, self.output_layer.weights_from_previous_to_this)
        )
        if test:
            print("--")
            print(inputs)
            print(hidden_output)
            print(output)
            print("--")
        return hidden_output, output

    def print_weights(self):
        print("    Layer 1 (4 neurons, each with 3 inputs): ")
        print(self.hidden_layer.weights_from_previous_to_this)
        print("    Layer 2 (1 neuron, with 4 inputs):")
        print(self.output_layer.weights_from_previous_to_this)


if __name__ == "__main__":
    input_nodes = 2
    hidden_nodes = 4
    output_nodes = 1

    neural_network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes)

    training_set_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    training_set_outputs = np.array([[0, 1, 1, 0]]).T

    # training_set_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # training_set_outputs = np.array([[0, 1, 1, 0]]).T

    neural_network.train(training_set_inputs, training_set_outputs, 5000)
    hidden_state, output = neural_network.predict(np.array([0, 0]))
    print(output)
    hidden_state, output = neural_network.predict(np.array([0, 1]))
    print(output)
    hidden_state, output = neural_network.predict(np.array([1, 0]))
    print(output)
    hidden_state, output = neural_network.predict(np.array([1, 1]))
    print(output)
