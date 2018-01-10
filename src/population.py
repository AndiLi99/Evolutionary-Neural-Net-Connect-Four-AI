import numpy as np
from copy import copy, deepcopy
from individual import Individual
import fitness
import random

from conv_layer import ConvLayer, Filter
from dense_layer import DenseLayer
from softmax_layer import SoftmaxLayer

from operator import itemgetter

class Population:
    # Args:
    #   initial_pop (int): how many individuals should be in the population
    #   layer_types (string list): a list of strings indicating the structure of each individual (see individual.py
    #           for more detail)
    #   layer_shapes (tuple list): a list of list of tuples indicating the shape of each individual (see individual.py
    #           for more detail)
    #   population (list of individuals) optional: a list of individuals to be used
    def __init__(self, initial_pop, layer_types, layer_shapes, conv_layer_types=None, population=None):
        self.pop_size = initial_pop
        self.layer_types = layer_types
        self.layer_shapes = layer_shapes
        self.conv_layer_types = conv_layer_types

        if population is not None:
            self.population = population

            # If not enough members, create random ones
            if initial_pop < len(population):
                while initial_pop < len(population):
                    self.population.append(Individual(layer_types, layer_shapes, conv_layer_types))
            else:
                self.pop_size = len(population)

            self.fitness = zip(np.zeros(self.pop_size), range(self.pop_size))
        else:
            self.fitness = zip(np.zeros(initial_pop), range(initial_pop))

            self.population = []
            for i in range(initial_pop):
                self.population.append(Individual(layer_types, layer_shapes, conv_layer_types))

    # Evolves the population by selecting the top 25% and crossing over and mutating to create children
    # Args:
    #   games_played (int): the minimum number of games each network will play against other networks
    #   survival_chance (float) optional: the chance a random member will live to the next generation
    def evolve (self, games_played, survival_chance=0.1):
        # fitness is a 1D array of the fitness of each member
        self.fitness = zip(fitness.populationFitness(self.population, games_played), range(self.pop_size))
        self.fitness.sort(key=itemgetter(0))

        # Chance of population lives randomly
        survivors = [0 if random.random() > survival_chance else 1 for i in range(self.pop_size)]

        # Keep best 25%
        for i in range(0, self.pop_size/4):
            survivors [self.fitness[i][1]] = 1

        # Store who survives
        survivors_index = []
        for i in range(self.pop_size):
            if survivors[i] == 1:
                survivors_index.append(i)

        # Create and save new population
        newPop = []
        for i in range(len(survivors_index)):
            newPop.append(self.population[survivors_index[i]])
        while len(newPop) <= self.pop_size:
            newPop.append(crossover(self.population[survivors_index[random.randint(0, len(survivors_index) -1)]], self.population[survivors_index[random.randint(0, len(survivors_index) -1)]]))
        self.population = newPop

    # Sets a population
    # Args:
    #   population (list of Individuals): population to be used
    #   layer_sizes: list of layer sizes (syntax explained in individual.py)
    def set_population(self, population, layer_sizes):
        self.population = population
        self.pop_size = len(population)
        self.layer_sizes = layer_sizes

    # Saves population to a file
    # File format:
    #   1. number of individuals in population
    #   2. each individuals data
    #       a) number of layers
    #       b) each layers data
    #           i) layer type
    #           ii) layer shape
    #           iii) weight list
    #           iv) bias list
    def save (self, file_name):
        file = open(file_name, 'w')

        # Store population size
        file.write(str(self.pop_size) + "\n")

        # Store each individual
        for individual in self.population:
            layer_types = individual.get_layer_types()
            layer_shapes = individual.get_layer_shapes()
            layers = individual.get_layers()
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

# Mutates an individual
# Args:
#   individual ("Individual" object)- the individual to be mutated
#   mutate_range (float) optional - the maximum possible change for a parameter
#   mutate_chance (float) optional - the chance for a gene to be mutated

def mutate_individual(individual, mutate_range=0.1, mutate_chance=None):
    # Set mutation chance so on average, 1 gene is mutated (probability = 1/total num genes)
    if mutate_chance is None:
        mutate_chance = (1.0/individual.get_num_genes())*3.0
        print(mutate_chance)

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
                    print("mutating conv")
                    # Randomly select a maximum mutation value for both weights and biases (adds more variance)
                    mutate_w = random.random()*mutate_range
                    mutate_b = random.random()*mutate_range

                    # Mutations for weights and biases (range is (plus/minus) mutate values)
                    weight_mutation = (2*random.random()-1)*mutate_w*np.random.randn(f.get_filter_size()[0],f.get_filter_size()[1],f.get_filter_size()[2])
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
                    print("mutating dense")
                    # Randomly select a maximum mutation value for both weights and biases
                    mutate_w = random.random()*mutate_range
                    mutate_b = random.random()*mutate_range

                    # Mutate
                    weights[i] += (2*random.random()-1)*mutate_w*np.random.randn(l.get_layer_shape()[1])
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
                lyr.set_filter(index=i, filtr=deepcopy(parent.get_filter(i)))
            layers.append(lyr)
        elif lt == "dense" or lt == "soft":
            weights = []
            biases = []
            lyr = DenseLayer(layer_shape=ls[0])
            if lt == "soft":
                lyr = SoftmaxLayer(layer_shape=ls[0])

            # Loop for each neuron
            for i in range(ls[0][0]):
                parent = ml
                # Randomly pick either mother or father gene based on alpha
                if random.random() < alpha:
                    parent = fl
                weights.append(deepcopy(parent.get_weights(i)))
                biases.append(deepcopy(parent.get_biases(i)))
            lyr.set_weights_biases(weights, biases)
            layers.append(lyr)
    child = Individual(deepcopy(father.get_layer_types()), deepcopy(father.get_layer_shapes()), None, layers)
    child = mutate_individual(child)
    return child

# Loads population from a saved file
# File format:
#   1. number of individuals in population
#   2. each individuals data
#       a) number of layers
#       b) each layers data
#           i) layer type
#           ii) weight list
#           iii) bias list
def load_population(file_name):
    counter = 0
    file = open(file_name, 'r')
    #read line by line
    arr = file.read().splitlines()

    pop_size = int(arr[counter])
    counter += 1
    initial_pop = []

    for i in range(pop_size):
        layer_types = []
        layer_shapes = []
        layers = []

        num_layers = int(arr[counter])
        counter += 1

        for j in range(num_layers):
            type = arr[counter]
            layer_types.append(type)
            counter += 1

            if type == "conv":
                image_shape = (int(arr[counter]), int(arr[counter+1]), int(arr[counter+2]))
                counter += 3

                filter_shape = (int(arr[counter]), int(arr[counter+1]), int(arr[counter+2]), int(arr[counter+3]))
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

                layers.append(ConvLayer(image_shape, filter_shape, None, 0, filters))

            elif type == "dense" or type == "soft":
                shpe = (int(arr[counter]), int(arr[counter+1]))
                layer_shapes.append([shpe])
                counter += 2

                weights = np.zeros(shpe)
                biases = np.zeros(shpe[0])

                for cl in range(shpe[0]):
                    for pl in range(shpe[1]):
                        weights[cl][pl] = float(arr[counter])
                        counter+=1

                for cl in range(shpe[0]):
                    biases[cl] = float(arr[counter])
                    counter+=1

                if type == "dense":
                    layers.append(DenseLayer(shpe, weights, biases))
                elif type == "soft":
                    layers.append(SoftmaxLayer(shpe, weights, biases))

        initial_pop.append(Individual(layer_types, layer_shapes, None, layers))
    population = Population(pop_size, initial_pop[0].get_layer_types(), initial_pop[0].get_layer_shapes(), None, initial_pop)
    return population
