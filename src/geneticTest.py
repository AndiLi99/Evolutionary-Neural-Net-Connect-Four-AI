import genetic
import Fitness
import net
import numpy as np
import connectFour
from minimax import pickMove
import individual

pop = genetic.Pop(layer_types=["conv", "dense", "soft"], layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]], initial_pop=20)
pop.evolve(12)

net1 = pop.population[0]
net1.save("net1.txt")
pop.save("population.txt")
pop = genetic.load_population("population.txt")
net1 = pop.population[0]
net1.save("net1compare.txt")
net2 = individual.load("net1compare.txt")
net2.save("net2.txt")

net2 = pop.population[1]

while True:
    board = np.zeros((6,7))
    while(connectFour.checkWinner(board) ==2):
        move = input("make a move: ")
        if not connectFour.check_valid(board, move):
            continue
        # connectFour.play(board, 1, pickMove(board, 1, 2))
        connectFour.play(board, 1, move)
        connectFour.print_board(board)
        # raw_input("press")
        print
        if not connectFour.checkWinner(board)==2:
            break
        connectFour.play(board, -1, pickMove(board, -1, 3, net1))
        connectFour.print_board(board)
