import numpy as np

def sigmoid (z):
    for i in range(len(z)):
        if z[i] < -35:
            z[i] = 0.000000000001
        elif z[i] > 35:
            z[i] = 0.99999999999
        else:
            z[i] = 1/(1+np.exp(z[i]))
    return z

class DenseLayer:# -- Class for the dense layer
    # Args:
    #   layer_shape (tuple): a 2-tuple (number of neurons on current layer, number of neurons on previous layer)
    def __init__(self, layer_shape, weights=None, biases=None):
        self.layer_shape = layer_shape
        # Biases is a list biases for each neuron
        if biases:
            self.biases = biases
        else:
            self.biases = np.random.randn(layer_shape[0])

        # Weights is a 2D list w[x][y] where x is the neuron number in the current layer and
        # y is the neuron number on the previous layer
        if weights:
            self.weights = weights
        else:
            self.weights = np.random.randn(layer_shape[0], layer_shape[1])

    # Calculates the activation of the layer given a list of activations
    # Args:
    #   activations (1D np array): a np array with the activations in the previous layer
    def feed_forward(self, activations):
        return sigmoid(np.dot(self.weights, activations) + self.biases)

    # Returns all weights in the layer (2D Array)
    def get_all_weights(self):
        return self.weights

    # Returns all biases in the layer
    def get_all_biases(self):
        return self.biases

    # Returns weights in the layer connecting to a neuron (1D Array)
    def get_weights(self, index):
        return self.weights[index]

    # Returns all biases in the layer
    def get_biases(self, index):
        return self.biases[index]

    # Returns layer shape of network
    def get_layer_shape(self):
        return self.layer_shape

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
        self.weights = weights
        self.biases = biases
        self.layer_shape = (len(biases), len(weights[0]))
        return self.layer_shape
