from conv_layer import ConvLayer, Filter
from dense_layer import DenseLayer
from softmax_layer import SoftmaxLayer
import numpy as np

class Individual:
    # Args:
    #   layer_types (string list): a list of strings indicating which types of layers each should be
    #           for convolution layers, the string "conv" should be used
    #           for dense layers, the string "dense" should be used
    #           for softmax layers, the string "soft" should be used
    #   layer_shapes (list of lists of tuples): a list of lists of tuples indicating the shapes of each layer
    #           for convolution layers, a list should contain two seperate tuples (image shape, filter shape)
    #           for dense and softmax layers, a list should contain one individual tuple (layer shape)
    #   conv_layer_types (list of tuples) optional: a list of tuples (filter_method, zero padding) for customizing
    #           the type of filter methods to be used
    #   layers (list of Layer objects) optional: a list of layers to be used to load an individual network
    def __init__(self, layer_types, layer_shapes, conv_layer_types=None, layers=None):
        self.layer_types = layer_types
        self.layer_shapes = layer_shapes
        self.num_genes = 0
        if layers is not None:
            self.layers = layers
            for typ, shpe in zip(layer_types, layer_shapes):
                if typ == "conv":
                    self.num_genes += shpe[1][0]
                elif typ == "dense":
                    self.num_genes += shpe[0][0]
                elif typ == "soft":
                    self.num_genes += shpe[0][0]
        else:
            self.layers = []
            cntr = 0
            n_conv_layer_types = len(conv_layer_types)
            for typ, shpe in zip(layer_types, layer_shapes):
                if typ == "conv":
                    if cntr >= n_conv_layer_types:
                        self.layers.append(ConvLayer(image_shape=shpe[0],
                                                     filter_shape=shpe[1],
                                                     filter_method=conv_layer_types[cntr][0],
                                                     zero_padding=conv_layer_types[cntr][1]))
                        cntr += 1
                    else:
                        self.layers.append(ConvLayer(image_shape=shpe[0],
                                                     filter_shape=shpe[1]))
                    self.num_genes += shpe[1][0]
                elif typ == "dense":
                    self.layers.append(DenseLayer(layer_shape=shpe[0]))
                    self.num_genes += shpe[0][0]
                elif typ == "soft":
                    self.layers.append(SoftmaxLayer(layer_shape=shpe[0]))
                    self.num_genes += shpe[0][0]

    # Returns the output of the network given an input
    # Args:
    #   input_layer (np array): the input
    def feed_forward(self, input_layer):
        is_conv_layer = True
        if not self.layer_types[0] == 'conv':
            is_conv_layer = False
        elif self.layer_types[0] == 'conv':
            if len(input_layer.shape) == 2:
                input_layer = np.array([input_layer])

        for lyr, typ in zip(self.layers, self.layer_types):
            if typ == 'dense' or typ == 'soft':
                # Squash input if previous layer is convolutional
                if is_conv_layer == True:
                    l = np.array([])
                    for x in input_layer:
                        l = np.concatenate((l,x.ravel()))

                    input_layer = l.ravel()
                    is_conv_layer = False
            input_layer = lyr.feed_forward(input_layer)
        return input_layer

    def get_layers(self):
        return self.layers

    def get_layer_types(self):
        return self.layer_types

    def get_layer_shapes(self):
        return self.layer_shapes

    def get_num_genes(self):
        return self.num_genes

    def set_layers(self, layer_types, layer_shapes, layers):
        self.layer_types = layer_types
        self.layer_shapes = layer_shapes
        self.layers = layers
        self.num_genes = 0
        for lt, l in zip(layer_types, layers):
            if lt == "conv":
                self.num_genes += l.get_num_filters()
            elif lt == "dense" or lt == "soft":
                self.num_genes += l.get_num_neurons()

    def save(self, filename):
        file = open(filename, 'w')

        layer_types = self.get_layer_types()
        layer_shapes = self.get_layer_shapes()
        layers = self.get_layers()
        num_layers = len(layer_types)

        # Store number of layers
        file.write(str(num_layers) + "\n")

        for lt, ls, l in zip(layer_types, layer_shapes, layers):
            # Store layer type
            file.write(lt + "\n")
            if lt == "conv":
                # Store layer shape
                for x in ls:
                    for y in x:
                        file.write(str(y) + "\n")
                # Store filters
                for f in l.get_all_filters():
                    w = f.get_weights()
                    b = f.get_bias()

                    for i in w:
                        for j in i:
                            for k in j:
                                file.write(str(k) + "\n")

                    file.write(str(b) + "\n")
            elif lt == "dense" or lt == "soft":
                # Store layer shape
                for x in ls[0]:
                    file.write(str(x) + "\n")


                # Store weights
                for w in l.get_all_weights():
                    for i in w:
                        file.write(str(i) + "\n")

                # Store biases
                for b in l.get_all_biases():
                    file.write(str(b) + "\n")

        file.close()

def load (filename):
    counter = 0
    file = open(filename, 'r')
    # read line by line
    arr = file.read().splitlines()

    layer_types = []
    layer_shapes = []
    layers = []

    num_layers = int(arr[counter])
    counter += 1

    for i in range(num_layers):
        typ = arr[counter]
        layer_types.append(typ)
        counter += 1

        if typ == "conv":
            image_shape = (int(arr[counter]), int(arr[counter + 1]), int(arr[counter + 2]))
            counter += 3

            filter_shape = (int(arr[counter]), int(arr[counter + 1]), int(arr[counter + 2]), int(arr[counter + 3]))
            counter += 4

            layer_shapes.append([image_shape, filter_shape])
            filters = []

            for i in range(filter_shape[0]):
                weights = np.zeros(filter_shape[1:])
                bias = 0

                for i in range(filter_shape[1]):
                    for j in range(filter_shape[2]):
                        for k in range(filter_shape[3]):
                            weights[i][j][k] = float(arr[counter])
                            counter += 1
                bias = float(arr[counter])
                counter += 1

                filters.append(Filter(filter_shape[1:], weights, bias))

            layers.append(ConvLayer(image_shape, filter_shape, filters))

        elif typ == "dense" or typ == "soft":
            shpe = (int(arr[counter]), int(arr[counter + 1]))
            layer_shapes.append([shpe])
            counter += 2

            weights = np.zeros(shpe)
            biases = np.zeros(shpe[0])

            for cl in range(shpe[0]):
                for pl in range(shpe[1]):
                    weights[cl][pl] = float(arr[counter])
                    counter += 1

            for cl in range(shpe[0]):
                biases[cl] = float(arr[counter])
                counter += 1

            if typ == "dense":
                layers.append(DenseLayer(shpe, weights, biases))
            elif typ == "soft":
                layers.append(SoftmaxLayer(shpe, weights, biases))
    return Individual(layer_types, layer_shapes, layers)