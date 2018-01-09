import genetic
import Fitness
import numpy as np
import connectFour
from minimax import pickMove
import individual
import random

pop = genetic.Pop(layer_types=["conv", "dense", "soft"], layer_shapes=[[(1, 6, 7), (4, 1, 4, 4)], [(20, 4*3*4)], [(2, 20)]], initial_pop=50)
# for i in range(1000000):
#     pop.evolve(25)
#     if i%100 == 0:
#         string = "pop_gen"+ str(i)
#         pop.save(string)


while True:
    net1 = pop.population[random.randint(0,49)]
    net2 = pop.population[random.randint(0,49)]
    board = np.zeros((6,7))
    print "Winner is: " + str(Fitness.compete (net1, net2))
    input()
    # while(connectFour.checkWinner(board) ==2):
    #     move = input("make a move: ")
    #     if not connectFour.check_valid(board, move):
    #         continue
    #     # connectFour.play(board, 1, pickMove(board, 1, 2))
    #     connectFour.play(board, 1, move)
    #     connectFour.print_board(board)
    #     # raw_input("press")
    #     print
    #     if not connectFour.checkWinner(board)==2:
    #         break
    #     connectFour.play(board, -1, pickMove(board, -1, 3, net1))
    #     connectFour.print_board(board)
