import numpy as np

def sigmoid (z):
    for i in range(len(z)):
        for j in range(len(z[i])):
            for k in range(len(z[i][j])):
                if z[i][j][k] < -35:
                    z[i][j][k] = 0.000000000001
                elif z[i][j][k] > 35:
                    z[i][j][k] = 0.99999999999
                else:
                    z[i][j][k] = 1/(1+np.exp(z[i][j][k]))
    return z

# Pads each image in a list of images with a specified amount of zeros
# Args:
#   image_list (np array): list of 2D images
#   zero_padding (int): number of zeros around the border of each image
def pad_with_zeros (image_list, zero_padding):
    n_i = len(image_list)
    h_i = len(image_list[0])
    l_i = len(image_list[0][0])
    zero_padded_images=np.zeros((n_i, h_i+2*zero_padding, l_i+2*zero_padding))
    zero_padded_images[:,zero_padding:h_i+zero_padding,zero_padding:l_i+zero_padding] = image_list
    return zero_padded_images

# Convolution layer
class ConvLayer:
    # Args:
    #   image_shape: a 3-tuple (num_images, image_height, image_length)
    #   filter_shape: a 4-tuple (num_filters, filter_depth, filter_height, filter_length)
    #   filter_method (string) optional: the way the filter should be applied
    #           "partial" to use the filter normally
    #           "full" to allow the filter to go outside of the image (returns a filtered image the same size)
    #   zero_padding (int) optional: number of zeros to be used around the border of an image if full filtering is used
    #   filters (list of Filters) optional: list of filters to be used if already saved
    def __init__(self, image_shape, filter_shape, filter_method="partial", zero_padding=0, filters=None):
        self.image_shape = image_shape
        self.filter_shape = filter_shape
        self.output_shape = (filter_shape[0], image_shape[1]-filter_shape[1]+1, image_shape[2]-filter_shape[2]+1)
        self.filter_method = filter_method
        self.zero_padding = zero_padding

        # Create list of filter objects
        if filters is not None:
            self.filters = filters
        else:
            self.filters = []
            for i in range(filter_shape[0]):
                self.filters.append(Filter(self.filter_shape[1:]))

    # Forwards past a list of images and returns the new list of images
    def feed_forward (self, image_list):
        new_image_list = []
        if self.filter_method=="full":
            image_list = pad_with_zeros(image_list, self.zero_padding)

        for i in range(self.filter_shape[0]):
            fil = self.filters[i]
            feature_image = fil.use_filter(image_list)
            new_image_list.append(feature_image)
        return sigmoid(new_image_list)

    def get_num_filters(self):
        return self.filter_shape[0]

    def get_filter(self, index):
        return self.filters[index]

    def get_all_filters(self):
        return self.filters

    def get_output_shape(self):
        return self.output_shape

    def set_filter(self, index, filtr):
        self.filters[index] = filtr

    def set_all_filters(self, filters):
        self.filters = filters

# Individual filter objects
class Filter:
    # Args:
    #   filter_size: a 3-tuple (filter_depth, filter_height, filter_length)
    def __init__(self, filter_size, weights=None, bias=None):
        self.filter_size = filter_size
        self.feature_map_length = filter_size[2]
        self.feature_map_height = filter_size[1]
        self.num_feature_maps = filter_size[0]
        if weights is not None:
            self.weights = weights
        else:
            self.weights = [np.random.randn(self.feature_map_height, self.feature_map_length) for f in range(self.num_feature_maps)]

        if bias is not None:
            self.bias = bias
        else:
            self.bias = np.random.random()

    # Takes in a list of images and applies the filter specific to the object to the filter, returning the new 2D image
    # Args:
    #   image_list: a list of 2D images
    def use_filter (self, image_list):
        num_images = len(image_list)
        # Partial filter method
        new_image_size = (len(image_list[0]) - self.feature_map_height + 1, len(image_list[0][0]) - self.feature_map_length + 1)
        new_image = np.zeros(new_image_size)
        for i in range(num_images):
            new_image += self.use_feature_map(self.weights[i], new_image_size, image_list[i])
        for y in range(new_image_size[0]):
            for x in range(new_image_size[1]):
                new_image[y][x] = new_image[y][x]+ self.bias
        return new_image


    # This method takes in a feature map and slides it across an image
    # Returns:
    #   a 2D array which is the new output image
    def use_feature_map (self, feature_map, new_image_size, image):
        new_image = np.zeros(new_image_size)
        for x in range(new_image_size[1]):
            for y in range(new_image_size[0]):
                img_piece = image[y:y+self.feature_map_height,x:x+self.feature_map_length]
                new_image[y][x] = np.dot(feature_map.ravel(), img_piece.ravel())
        return new_image

    def get_filter_size(self):
        return self.filter_size

    def get_weights(self):
        return self.weights

    def get_bias(self):
        return self.bias

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias