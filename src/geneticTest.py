import population
import fitness
import numpy as np
import connectFour
from minimax import pickMove
import individual
import random

pop = population.Population(initial_pop=20, layer_types=["conv", "dense", "soft"],
                            layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]],
                            conv_layer_types=[("partial",2)])
# pop.save("test1.txt")
# print(pop.population[10].get_layers()[0].get_filter(2).get_weights())
# p2 = population.load_population("test1.txt")
#
# p2.save("test2.txt")
# print(p2.population[10].get_layers()[0].get_filter(2).get_weights())
# net = pop.population[0]
# net.save("net100.txt")

for x in range(0, 1000000):
    pop.evolve(12)
    print("gen " + str(x))
    # if x%2 == 0:
    #     pop.save("pop_gen"+str(x)+".txt")
    pop.save("pop_gen" + str(x) + ".txt")
