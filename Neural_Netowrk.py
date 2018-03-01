import numpy as np


class NeuronLayer:
    def __init__(self, neurons, neurons_in_previous_layer):
        import time
        np.random.seed(int(time.time()))
        self.bias = np.random.random()
        self.weights_from_previous_to_this = 2 * np.random.random((neurons_in_previous_layer, neurons)) - self.bias


class NeuralNetwork:
    def __init__(self, hidden_layer, output_layer):
        self.hidden_layer = hidden_layer
        self.output_layer = output_layer

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

    hidden_layer = NeuronLayer(hidden_nodes, input_nodes)
    output_layer = NeuronLayer(output_nodes, hidden_nodes)
    neural_network = NeuralNetwork(hidden_layer, output_layer)

    # training_set_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # training_set_outputs = np.array([[0, 1, 1, 0]]).T

    # training_set_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # training_set_outputs = np.array([[0, 1, 1, 0]]).T

    # neural_network.train(training_set_inputs, training_set_outputs, 5000)
    # hidden_state, output = neural_network.predict(np.array([0, 0]))
    # print(output)
    # hidden_state, output = neural_network.predict(np.array([0, 1]))
    # print(output)
    # hidden_state, output = neural_network.predict(np.array([1, 0]))
    # print(output)
    # neural_network.print_weights()
    # hidden_state, output = neural_network.predict(np.array([100, 123]))
    # print(output)
