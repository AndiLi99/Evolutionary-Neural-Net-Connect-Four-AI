import genetic
import Fitness
import net

pop = genetic.Pop(layer_types=["conv", "dense", "soft"], layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]], initial_pop=50)
pop.evolve(25)
# for i in range(100000):
#     pop.evolve(25)
#     print i
#     if i%100 == 0:
#         string = "pop_gen" + str(i) + ".txt"
#         pop.save_population(string)
#
# pop = genetic.load_population("pop_gen2600.txt")
# net = pop.population[0]
# net.write_to_file("net_gen2600.txt")
