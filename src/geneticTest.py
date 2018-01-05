import genetic
import Fitness
import net

pop = genetic.Pop([42,30,1], 100)

for i in range(1000000000):
    pop.evolve(50)
    print i
    if i%100 == 0:
        string = "pop_gen" + str(i) + ".txt"
        pop.save_population(string)
