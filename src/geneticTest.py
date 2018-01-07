import genetic
import Fitness
import numpy as np
import connectFour
from minimax import pickMove
import individual

pop = genetic.Pop(layer_types=["conv", "dense", "soft"], layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]], initial_pop=20)
pop = genetic.load_population("pop_gen20.txt")
net = pop.population[1]
net.save("net20.txt")

for x in range(100000000):
    pop.evolve(12)
    if x%20 == 0:
        pop.save("pop_gen"+str(x)+".txt")
