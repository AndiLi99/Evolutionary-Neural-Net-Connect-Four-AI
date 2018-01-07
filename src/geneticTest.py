import population
import fitness
import numpy as np
import connectFour
from minimax import pickMove
import individual

pop = population.Population(layer_types=["conv", "dense", "soft"], layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]], initial_pop=20)
pop = population.load_population("pop_gen0.txt")
# net = population.population[1]
# net.save("net20.txt")

for x in range(100000000):
    pop.evolve(12)
    print("gen " + str(x))
    if x%10 == 0:
        pop.save("pop_gen"+str(x)+".txt")
    #pop.save("pop_gen" + str(x) + ".txt")