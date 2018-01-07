from conv_layer import ConvLayer
from dense_layer import DenseLayer
from softmax_layer import SoftmaxLayer
import numpy as np
from copy import deepcopy

class Individual:
    # Args:
    #   layer_types (string list): a list of strings indicating which types of layers each should be
    #           for convolution layers, the string "conv" should be used
    #           for dense layers, the string "dense" should be used
    #           for softmax layers, the string "soft" should be used
    #   layer_shapes (list of tuple-lists): a list of tuple-lists indicating the shapes of each layer
    #           for convolution layers, a list should contain two seperate tuples (image shape, filter shape)
    #           for dense and softmax layers, a list should contain one individual tuple (layer shape)
    def __init__(self, layer_types, layer_shapes, layers=None):
        self.layer_types = layer_types
        self.layer_shapes = layer_shapes
        self.num_genes = 0
        if not layers:
            self.layers = []
            for type, shpe in zip(layer_types, layer_shapes):
                if type == "conv":
                    self.layers.append(ConvLayer(shpe[0], shpe[1]))
                    self.num_genes += shpe[1][0]
                elif type == "dense":
                    self.layers.append(DenseLayer(shpe[0]))
                    self.num_genes += shpe[0]
                elif type == "soft":
                    self.layers.append(SoftmaxLayer(shpe[0]))
                    self.num_genes += shpe[0]
        else:
            self.layers = layers

    # Returns the output of the network given an input
    # Args:
    #   input_layer (np array): the input
    def forward_pass(self, input_layer):
        is_conv_layer = True
        if not self.layer_types[0] == 'conv':
            is_conv_layer = False
        elif self.layer_types[0] == 'conv':
            if len(input_layer.shape) == 2:
                input = np.array(input_layer)

        for lyr, type in zip(self.layers, self.layer_types):
            if type == 'dense' or type == 'soft':
                # Squash input if previous layer is convolutional
                if is_conv_layer == True:
                    input_layer = input_layer.flatten()
                    is_conv_layer = False

            input_layer = lyr.forward_pass(input_layer)
        return input_layer

    def get_layers(self):
        return deepcopy(self.layers)

    def get_layer_types(self):
        return deepcopy(self.layer_types)

    def get_layer_shapes(self):
        return deepcopy(self.layer_shapes)

    def get_num_genes(self):
        return self.num_genes

    def set_layers(self, layer_types, layer_shapes, layers):
        self.layer_types = deepcopy(layer_types)
        self.layer_shapes = deepcopy(layer_shapes)
        self.layers = deepcopy(layers)
        self.num_genes = 0
        for lt, l in zip(layer_types, layers):
            if lt == "conv":
                self.num_genes += l.get_num_filters()
            elif lt == "dense" or lt == "soft":
                self.num_genes += l.get_num_neurons()
