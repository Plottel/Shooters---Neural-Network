import random
import Params
import math


def sigmoid(output, activation_response):
    return 1 / (1 + math.exp(-output / activation_response))

    ###############################################
    ###               NEURON CLASS              ###
    ###############################################

# Represents an individual node in the Neural Network.
# Receives a number of inputs with corresponding weights.
class Neuron:
    # Creates randomised value representing input weights.
    # When a Neuron is created, its inputs are randomised.
    def randomise_weights(self):
        # 1 extra weight represents the threshold value.
        # This way allows the threshold to be built into the weights,
        # simplifying the math and allowing the GA to easily manipulate it.
        for i in range(self.num_inputs):
            self.input_weights.append(random.uniform(-1, 1))

    def __init__(self, num_inputs):
        # Member variables
        self.num_inputs = num_inputs + 1
        self.input_weights = []

        self.randomise_weights()


        ###############################################
        ###               NEURON LAYER CLASS        ###
        ###############################################

# Represents a collection of Neurons - a layer in the Neural Network.
# Used for both Hidden layers and Output layer.
class NeuronLayer:
    # Initialises neuron list
    def populate_neurons(self):
        for i in range(self.num_neurons):
            self.neurons.append(Neuron(self.num_inputs_per_neuron))

    def __init__(self, num_neurons, num_inputs_per_neuron):
        # Member variables
        self.num_neurons = num_neurons
        self.num_inputs_per_neuron = num_inputs_per_neuron
        self.neurons = []

        self.populate_neurons()


        ###############################################
        ###               NEURAL NET CLASS          ###
        ###############################################

# Co-ordinates the Neural Network
# Stores each layer of neurons
# Replaces weights after each iteration
class NeuralNet:
    num_inputs = Params.num_inputs
    num_outputs = Params.num_outputs
    num_hidden_layers = Params.num_hidden_layers
    neurons_per_hidden_layer = Params.neurons_per_hidden_layer
    layers = []

    # Sets up each layer of the neural network.
    # Initialises weights to random values between -1 and 1.
    def create_net(self):
        # Create first hidden layer.
        # This receives its input from the input layer, therefore its num_inputs == NeuralNet.num_inputs
        self.layers.append(NeuronLayer(self.neurons_per_hidden_layer, self.num_inputs))

        # Create remaining hidden layers.
        # These receive input from another hidden layer, therefore its num_inputs == NeuralNet.neurons_per_hidden_layer
        for i in range(self.num_hidden_layers - 1):
            self.layers.append(NeuronLayer(self.neurons_per_hidden_layer, self.neurons_per_hidden_layer))

        # Create output layer.
        # Its num_neurons == NeuralNet.num_outputs
        self.layers.append(NeuronLayer(self.num_outputs, self.neurons_per_hidden_layer))

    # Returns all the weights in the Network as a list.
    # Runs through each Weight in each Neuron in each Layer
    def get_weights(self):
        result = []

        # Loop through each layer.
        for layer in self.layers:
            # Loop through each neuron.
            for neuron in layer.neurons:
                # Loop through each weight.
                for weight in neuron.input_weights:
                    result.append(weight)

        return result

    # Returns the number of weights in the Network
    def get_number_of_weights(self):
        result = 0

        # Loop through each layer.
        for layer in self.layers:
            # Loop through each neuron.
            for neuron in layer.neurons:
                # Loop through each weight.
                for weight in neuron.input_weights:
                    result += 1

        return result

    # Replaces the weights in the Network with new ones.
    # Runs through each Weight in each Neuron in each Layer
    def replace_weights(self, weights):
        # The index of the weight currently being replaced
        cur_weight = 0

        # Loop through each layer.
        # This includes hidden layers and final output layer
        for layer in self.layers:
            # Loop through each Neuron in the layer
            for neuron in layer.neurons:
                # Loop through each weight in the neuron
                for k in range(neuron.num_inputs):
                    neuron.input_weights[k] = weights[cur_weight]
                    cur_weight += 1


    # This is the Network "loop".
    # Takes inputs, runs them through the Network, and calculates the resulting outputs.
    def update(self, inputs):
        # Used for each layer, the output from one layer becomes the inputs for the next.
        outputs = []

        # Loop through each layer.
        # This includes hidden layers and final output layer.
        for layer in self.layers:
            # On all layers except the first hidden layer, outputs become inputs for next layer.
            # Only the first hidden layer will avoid this condition.
            if layer.num_inputs_per_neuron != Params.num_inputs:
                inputs = outputs

            outputs = []
            cur_weight = 0

            # For each Neuron in the layer.
            for neuron in layer.neurons:
                tot_weighted_input = 0
                # For each input in the Neuron except last one.
                # Last input is the bias and therefore does not have a corresponding input
                for k in range(neuron.num_inputs - 1):
                    # Calculate the total weighted input.
                    tot_weighted_input += inputs[cur_weight] * neuron.input_weights[k]
                    cur_weight += 1

                # Add in the bias for this Neuron.
                # Bias is an extra weight with an input value of -1
                tot_weighted_input += neuron.input_weights[neuron.num_inputs - 1] * Params.bias

                output = sigmoid(tot_weighted_input, Params.activation_response)

                # Generate output value by running weighted input through Sigmoid function
                outputs.append(output)

                cur_weight = 0

        return outputs

    def __init__(self):
        self.layers = []
        self.create_net()