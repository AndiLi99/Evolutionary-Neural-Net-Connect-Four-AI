import numpy as np
from copy import deepcopy

def softmax (z):
    total = 0
    for i in range(len(z)):
        if z[i] < -20:
            z[i] = 0.0000000001
        elif z[i] > 23:
            z[i] = 9999999999.0
        else:
            z[i] = np.exp(z[i])
        total+= z[i]
    return z/total

class SoftmaxLayer:# -- Class for the softmax layer
    # Args:
    #   layer_shape (tuple): a 2-tuple (number of neurons on current layer, number of neurons on previous layer)
    def __init__(self, layer_shape):
        self.layer_shape = layer_shape
        # Biases is a list biases for each neuron
        self.biases = np.random.randn(layer_shape[0])

        # Weights is a 2D list w[x][y] where x is the neuron number in the current layer and
        # y is the neuron number on the previous layer
        self.weights = np.random.randn(layer_shape)

    # Calculates the activation of the layer given a list of activations
    # Args:
    #   activations (1D np array): a np array with the activations in the previous layer
    def feed_forward(self, activations):
        return softmax(np.dot(self.weights, activations) + self.biases)

    # Returns all weights in the layer (2D Array)
    def get_all_weights(self):
        return deepcopy(self.weights)

    # Returns all biases in the layer
    def get_all_biases(self):
        return deepcopy(self.biases)

    # Returns weights in the layer connecting to a neuron (1D Array)
    def get_weights(self, index):
        return deepcopy(self.weights[index])

    # Returns all biases in the layer
    def get_biases(self, index):
        return self.biases[index]

    # Returns all weights in the layer
    def get_layer_shape(self):
        return deepcopy(self.layer_shape)

    def get_num_neurons(self):
        return self.layer_shape[0]

    # Sets the weights and biases
    # Args:
    #   weights (2D np array): a np array of weights. Size of weights expected to be (number of neurons on current
    #       layer, number of neurons on previous layer)
    #   biases (1D np array): a np array of biases. Size of biases expected to be (number of neurons on current layer)
    # Returns:
    #   the shape of the layer created upon success
    #   error message upon failure
    def set_weights_biases (self, weights, biases):
        # Check that arrays are compatable
        if not len(weights) == len(biases):
            return "Failed to set parameters due to variance in weight and bias array sizes"
        self.weights = deepcopy(weights)
        self.biases = deepcopy(biases)
        self.layer_shape = (len(biases), len(weights[0]))
        return self.layer_shape