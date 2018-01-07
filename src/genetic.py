import numpy as np
from copy import copy, deepcopy
from individual import Individual
import Fitness
import random

from conv_layer import ConvLayer, Filter
from dense_layer import DenseLayer
from softmax_layer import SoftmaxLayer

from operator import itemgetter

class Pop:
    def __init__(self, layer_types, layer_shapes, initial_pop):
        self.population = []
        self.pop_size = initial_pop
        self.fitness = zip(np.zeros(initial_pop), range(initial_pop))
        self.layer_types = layer_types
        self.layer_shapes = layer_shapes
        for i in range(initial_pop):
            self.population.append(Individual(layer_types, layer_shapes))

    def evolve (self, games_played):
        #fitness is a 1D array of the fitness of each member
        self.fitness = zip(Fitness.populationFitness(self.population, games_played), range(self.pop_size))
        # self.fitness = zip(np.random.randn(self.pop_size), range(self.pop_size))
        self.fitness.sort(key=itemgetter(0))

        #10% chance of population lives randomly
        survivors = [0 if random.random() > 0.1 else 1 for i in range(self.pop_size)]

        for i in range(0, self.pop_size/4):
            survivors [self.fitness[i][1]] = 1

        survivors_index = []
        for i in range(self.pop_size):
            if survivors[i] == 1:
                survivors_index.append(i)

        newPop = []
        for i in range(len(survivors_index)):
            newPop.append(self.population[survivors_index[i]])
        while len(newPop) <= self.pop_size:
            mutated_net = self.mutate_individual(newPop[random.randint(0, len(survivors_index)-1)])
            newPop.append(mutated_net)
        self.population = newPop

    def print_pop(self):
        for i, pop in enumerate(self.population):
            print(self.population[i].getID())

    # Mutates an individual
    # Args:
    #   individual ("Individual" object)- the individual to be mutated
    #   mutate_range (float) optional - the maximum possible change for a parameter
    #   mutate_chance (float) optional - the chance for a gene to be mutated
    @staticmethod
    def mutate_individual(self, individual, mutate_range=0.1, mutate_chance=None):
        # Set mutation chance so on average, 1 gene is mutated (probability = 1/total num genes)
        if not mutate_chance:
            mutate_chance = 1.0/individual.get_num_genes()

        # Stores data for new mutated individual
        layer_types = individual.get_layer_types()
        layer_shapes = individual.get_layer_shapes()
        layers = individual.get_layers()

        # Loop for each layer
        for lt, l in zip(layer_types, layers):
            # If layer type is convolutional
            if lt == "conv":
                # Retrieve all filters for the layer
                filters = l.get_all_filters()

                for i, f in enumerate(filters):
                    # Randomly select filters to be mutated
                    if random.random() < mutate_chance:
                        # Randomly select a maximum mutation value for both weights and biases (adds more variance)
                        mutate_w = random.random()*mutate_range
                        mutate_b = random.random()*mutate_range

                        # Mutations for weights and biases (range is (plus/minus) mutate values)
                        weight_mutation = (2*random.random()-1)*mutate_w*np.random.randn(f.get_filter_size())
                        bias_mutation = (2*random.random()-1)*mutate_b

                        # Mutate
                        f.set_weights(f.get_weights()+weight_mutation)
                        f.set_bias(f.get_bias()+bias_mutation)

                        # Set mutated filter
                        l.set_filter(i, f)
            # If layer is dense or softmax
            elif lt == "dense" or lt == "soft":
                # Retrieve weights and biases for layer
                weights = l.get_all_weights()
                biases = l.get_all_biases()

                for i in range(len(biases)):
                    # Randomly select neurons whose weights and biases are to be mutated
                    if random.random() < mutate_chance:
                        # Randomly select a maximum mutation value for both weights and biases
                        mutate_w = random.random()*mutate_range
                        mutate_b = random.random()*mutate_range

                        # Mutate
                        weights[i] += (2*random.random()-1)*mutate_w*np.random.randn(l.get_layer_shape[1])
                        biases[i] += (2*random.random()-1)*mutate_b

                # Set weights and biases
                l.set_weights_biases(weights, biases)

        #Set mutations for individual
        individual.set_layers(layer_types, layer_shapes, layers)

        return individual

    # Creates a child from a mother and father
    # Args:
    #   father (individual) - a parent
    #   mother (individual) - a parent
    #   alpha (float) - chance to select gene from father, (1-alpha) chance from mother
    @staticmethod
    def crossover (father, mother, alpha=0.5):
        layers = []
        for lt, ls, fl, ml in zip(father.get_layer_types(), father.get_layer_shapes(),
                                  father.get_layers(), mother.get_layers()):
            if lt == "conv":
                lyr = ConvLayer(image_shape=ls[0], filter_shape=ls[1])
                # Loop for each filter
                for i in range(ls[1][0]):
                    parent = ml
                    # Randomly pick either mother or father gene based on alpha
                    if random.random() < alpha:
                        parent = fl
                    lyr.set_filter(index=i, filter=deepcopy(parent.get_filter(i)))
                layers.append(lyr)
            elif lt == "dense" or lt == "soft":
                weights = []
                biases = []
                lyr = DenseLayer(layer_shape=ls[0])
                if lt == "soft":
                    lyr = SoftmaxLayer(layer_shape=ls[0])

                # Loop for each neuron
                for i in range(ls[0]):
                    parent = ml
                    # Randomly pick either mother or father gene based on alpha
                    if random.random() < alpha:
                        parent = fl
                    weights.append(deepcopy(parent.get_weights[i]))
                    biases.append(deepcopy(parent.get_biases[i]))
                lyr.set_weights_biases(weights, biases)
                layers.append(lyr)
        child = Individual(father.get_layer_types(), father.get_layer_shapes, layers)
        return child

    def set_population(self, population, layer_sizes):
        self.population = population
        self.pop_size = len(population)
        self.layer_sizes = layer_sizes

    def save (self, file_name):
        file = open(file_name, 'w')
        file.write(str(self.pop_size))
        for individual in self.population:
            layer_types = individual.get_layer_types()

            layer_shapes = individual.l
            file.write("\n"+str(len(l_s)))
            for x in l_s:
                file.write("\n" + str(x))
            w = net.get_weights()
            for a in w:
                for b in a:
                    for c in b:
                        file.write("\n" + str(c))

            b = net.get_biases()
            for a in b:
                for c in a:
                    file.write("\n" + str(c))
        file.close()
#
# def load_population(file_name):
#     counter = 0
#     file = open(file_name, 'r')
#     #read line by line
#     arr = file.read().splitlines()
#     pop_size = int(arr[counter])
#     counter +=1
#     pop = []
#     layer_sizes = []
#     for i in range(pop_size):
#         n_layers = int(arr[counter])
#         counter += 1
#         layer_sizes = []
#         for x in range(n_layers):
#             layer_sizes.append(int(arr[counter]))
#             counter += 1
#         biases = []
#         weights = []
#         for x in range(1, n_layers):
#             layer = []
#             for y in range(layer_sizes[x]):
#                 neuron = []
#                 for z in range(layer_sizes[x-1]):
#                     neuron.append(float(arr[counter]))
#                     counter += 1
#                 layer.append(neuron)
#             weights.append(layer)
#         for x in range (1, n_layers):
#             layer = []
#             for y in range(layer_sizes[x]):
#                 layer.append(float(arr[counter]))
#                 counter += 1
#             biases.append(layer)
#         file.close()
#         network = net.Net(layer_sizes)
#         network.set_weights_biases(weights, biases)
#         pop.append(network)
#     p = Pop([],0)
#     p.set_population(pop, layer_sizes)
#     return p
