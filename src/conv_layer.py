import numpy as np
from copy import deepcopy

# Convolution layer
class ConvLayer:
    # Args:
    #   image_shape: a 3-tuple (num_images, image_height, image_length)
    #   filter_shape: a 4-tuple (num_filters, filter_depth, filter_height, filter_length)
    def __init__(self, image_shape, filter_shape):
        self.image_shape = image_shape
        self.filter_shape = filter_shape
        self.output_shape = (filter_shape[0], image_shape[1]-filter_shape[1]+1, image_shape[2]-filter_shape[2]+1)

        # Create list of filter objects
        self.filters = []
        for i in range(filter_shape[0]):
            self.filters.append(Filter(self.filter_shape[1:]))

    # Forwards past a list of images and returns the new list of images
    def forward_pass (self, image_list):
        new_image_list = []
        for i in range(self.filter_shape[0]):
            fil = self.filters[i]
            feature_image = fil.use_filter(self.image_shape[1:], image_list)
        return new_image_list

    def get_num_filters(self):
        return self.filter_shape[0]

    def get_filter(self, index):
        return deepcopy(self.filters[index])

    def get_all_filters(self):
        return deepcopy(self.filters)

    def get_output_shape(self):
        return deepcopy(self.output_shape)

    def set_filter(self, index, filter):
        self.filters[index] = deepcopy(filter)

    def set_all_filters(self, filters):
        self.filters = deepcopy(filters)

# Individual filter objects
class Filter:
    # Args:
    #   filter_size: a 3-tuple (filter_depth, filter_height, filter_length)
    def __init__(self, filter_size):
        self.filter_size = filter_size
        self.feature_map_length = filter_size[2]
        self.feature_map_height = filter_size[1]
        self.num_feature_maps = filter_size[0]
        self.weights = np.random.randn(filter_size)
        self.bias = np.random.random

    # Takes in a list of images and applies the filter specific to the object to the filter, returning the new 2D image
    # Args:
    #   image_shape: a 3-tuple (num_images, image_height, image_length)
    #   image_list: a list of 2D images
    def use_filter (self, image_shape, image_list):
        num_images = image_shape[0]
        new_image_size = (image_shape[1] - self.feature_map_height + 1, image_shape[2] - self.feature_map_length + 1)
        new_image = np.zeros(new_image_size)
        for i in range(num_images):
            new_image += self.use_feature_map(self.weights[i], image_list[i])
        for y in range(new_image_size[0]):
            for x in range(new_image_size[1]):
                new_image[y][x] += self.bias
        return new_image


    # This method takes in a feature map and slides it across an image
    # Returns:
    #   a 2D array which is the new output image
    def use_feature_map (self, feature_map, new_image_size, image):
        new_image = np.zeros(new_image_size)
        for x in range(new_image_size[1]):
            for y in range(new_image_size[0]):
                img_piece = image[y:y+self.feature_map_height, x:x+self.feature_map_length]
                new_image_size[y][x] = np.dot(feature_map.ravel(), img_piece.ravel())
        return new_image

    def get_filter_size(self):
        return self.filter_size

    def get_weights(self):
        return self.weights

    def get_biases(self):
        return self.bias

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias