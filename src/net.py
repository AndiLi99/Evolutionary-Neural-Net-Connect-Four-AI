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

# -- Class for the neural network
class Net:
    def __init__(self, layer_sizes, ID=-1):
        self.__layer_sizes = layer_sizes
        self.__n_layers = len(layer_sizes)
        self.__ID = ID
        # Biases is a 2D array with each layers biases. The input and output layer have no biases
        self.__biases = [np.zeros(l) for l in layer_sizes[1:]]
        # Weights is a 3D array w[x][y][z] where x is the layer number, y is the neuron on layer x, and z is the weight
        # connecting neuron z on layer x-1 to neuron y in layer x
        self.__weights = [np.zeros((cl, pl)) for pl, cl in zip(self.__layer_sizes[:self.__n_layers-1], self.__layer_sizes[1:])]

    def feed_forward_wrapper(self, board):
        board = np.reshape(board, 42)
        return self.feed_forward(board)
    # Returns next activation, the z value
    def __next_activation(self, curr_activations, curr_layer):
        return np.dot(self.__weights[curr_layer], curr_activations) + self.__biases[curr_layer]

    # Returns output of neural net given an input
    def feed_forward (self, input_layer):
        for l in range(0, self.__n_layers-1):
            input_layer = sigmoid(self.__next_activation(input_layer, l))
        return input_layer

    def getID(self):
        return self.__ID

    def setID(self, ID):
        self.__ID = ID
    # Returns all weights in the neural network (3D Array)
    def get_weights(self):
        return self.__weights

    # Returns all biases in the neural network (2D Array)
    def get_biases(self):
        return self.__biases

    def get_layer_sizes(self):
        return self.__layer_sizes

    def set_weights_biases (self, weights, biases):
        if not len(weights) == len(biases):
            return "failed"
        n_layers = len(weights) + 1
        layer_sizes = []
        layer_sizes.append(len(weights[0][0]))
        for w in weights[0]:
            if not len(w) == layer_sizes[0]:
                return "failed"
        for l, b, n in zip(weights, biases, range(0, n_layers-1)):
            if len(l) == len(b):
                layer_sizes.append(len(b))
                for w in l:
                    if not len(w) == layer_sizes[n]:
                        return "failed"
            else:
                return "failed"
        self.__n_layers = n_layers
        self.__weights = weights
        self.__biases = biases
        self.__layer_sizes = layer_sizes
        return layer_sizes

    def large_weight_initializer(self):
        """Initialize the weights using a Gaussian distribution with mean 0
        and standard deviation 1.  Initialize the biases using a
        Gaussian distribution with mean 0 and standard deviation 1.

        Note that the first layer is assumed to be an input layer, and
        by convention we won't set any biases for those neurons, since
        biases are only ever used in computing the outputs from later
        layers.

        This weight and bias initializer uses the same approach as in
        Chapter 1, and is included for purposes of comparison.  It
        will usually be better to use the default weight initializer
        instead.

        """
        self.__biases = [np.random.randn(y) for y in self.__layer_sizes[1:]]
        self.__weights = [np.random.randn(y, x)
                        for x, y in zip(self.__layer_sizes[:-1], self.__layer_sizes[1:])]

    def write_to_file (self, filename):
        file = open(filename, 'w')
        l_s = self.get_layer_sizes()
        file.write(str(len(l_s)))
        for x in l_s:
            file.write("\n" + str(x))
        w = self.get_weights()
        for a in w:
            for b in a:
                for c in b:
                    file.write("\n" + str(c))

        b = self.get_biases()
        for a in b:
            for c in a:
                file.write("\n" + str(c))

        file.close()

def load (filename):
    counter = 0
    file = open(filename, 'r')
    #read line by line
    arr = file.read().splitlines()
    n_layers = int(arr[counter])
    layer_sizes = []
    for x in range(n_layers):
        counter += 1
        layer_sizes.append(int(arr[counter]))
    biases = []
    weights = []
    for x in range(1, n_layers):
        layer = []
        for y in range(layer_sizes[x]):
            neuron = []
            for z in range(layer_sizes[x-1]):
                counter += 1
                neuron.append(float(arr[counter]))
            layer.append(neuron)
        weights.append(layer)
    for x in range (1, n_layers):
        layer = []
        for y in range(layer_sizes[x]):
            counter += 1
            layer.append(float(arr[counter]))
        biases.append(layer)
    file.close()
    network = Net(layer_sizes)
    network.set_weights_biases(weights, biases)
    return network
