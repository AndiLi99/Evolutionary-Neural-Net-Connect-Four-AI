import numpy as np
from copy import copy, deepcopy
import net
import Fitness
import random

from operator import itemgetter

class Pop:
    def __init__(self, layer_sizes, initial_pop):
        self.latest_ID = 0
        self.population = []
        self.pop_size = initial_pop
        self.fitness = zip(np.zeros(initial_pop), range(initial_pop))
        self.layer_sizes = layer_sizes
        for i in range(initial_pop):
            self.population.append(net.Net(layer_sizes, self.latest_ID))
            self.latest_ID+=1
        self.random_pop()

    def evolve (self, alpha):
        #fitness is a 1D array of the fitness of each member
        self.fitness = zip(Fitness.populationFitness(self.population, alpha), range(0,self.pop_size))
        # self.fitness = zip(np.random.randn(self.pop_size), range(self.pop_size))
        self.fitness.sort(key=itemgetter(0))

        #10% chance of population lives randomly
        survivors = [0 if random.random > 0.1 else 1 for i in range(self.pop_size)]

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

    def random_pop(self):
        for i,pop in enumerate(self.population):
            self.population[i].large_weight_initializer()
        return self.population

    def mutate_individual(self, parent_network, mutate_range=0.05):
        network = net.Net(self.layer_sizes, self.latest_ID)
        self.latest_ID+=1

        init_w_rng = random.random()*mutate_range
        init_b_rng = random.random()*mutate_range
        we = deepcopy(parent_network.get_weights())
        bi = deepcopy(parent_network.get_biases())
        for a in range(len(we)):
            for b in range(len(we[a])):
                for c in range(len(we[a][b])):
                    we[a][b][c] += init_w_rng*(2*random.random() - 1)
        for a in range(len(bi)):
            for b in range(len(bi[a])):
                bi[a][b] += init_b_rng*(2*random.random() - 1)
        network.set_weights_biases(we, bi)
        return network

    def set_population(self, population, layer_sizes):
        self.population = population
        self.pop_size = len(population)
        self.layer_sizes = layer_sizes

    def save_population(self, file_name):
        file = open(file_name, 'w')
        file.write(str(self.pop_size))
        for net in self.population:
            l_s = net.get_layer_sizes()
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

def load_population(file_name):
    counter = 0
    file = open(file_name, 'r')
    #read line by line
    arr = file.read().splitlines()
    pop_size = int(arr[counter])
    counter +=1
    pop = []
    layer_sizes = []
    for i in range(pop_size):
        n_layers = int(arr[counter])
        counter += 1
        layer_sizes = []
        for x in range(n_layers):
            layer_sizes.append(int(arr[counter]))
            counter += 1
        biases = []
        weights = []
        for x in range(1, n_layers):
            layer = []
            for y in range(layer_sizes[x]):
                neuron = []
                for z in range(layer_sizes[x-1]):
                    neuron.append(float(arr[counter]))
                    counter += 1
                layer.append(neuron)
            weights.append(layer)
        for x in range (1, n_layers):
            layer = []
            for y in range(layer_sizes[x]):
                layer.append(float(arr[counter]))
                counter += 1
            biases.append(layer)
        file.close()
        network = net.Net(layer_sizes)
        network.set_weights_biases(weights, biases)
        pop.append(network)
    p = Pop([],0)
    p.set_population(pop, layer_sizes)
    return p
