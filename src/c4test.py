import connectFour
import individual
import sys
import Fitness
import numpy as np
import minimax
import genetic
import random

pop0 = genetic.load_population("pop_gen0.txt")
pop20 = genetic.load_population("pop_gen20.txt")
pop40 = genetic.load_population("pop_gen40.txt")


w = 0
t = 0
l = 0
for k in range(20):
    board = np.zeros((6,7))
    net40 = pop40.population[random.randint(0,19)]
    net0 = pop0.population[random.randint(0,19)]
    while(connectFour.checkWinner(board) ==2):
        move = 1#input("make a move: ")
        if not connectFour.check_valid(board, move):
            continue
        connectFour.play(board, 1, minimax.pickMove(board, 1, 3, net40))
        # connectFour.play(board, 1, move)
        #connectFour.print_board(board)
        # raw_input("press")
        #print
        if not connectFour.checkWinner(board)==2:
            break
        connectFour.play(board, -1, minimax.pickMove(board, -1, 3, net0))
        #connectFour.print_board(board)
    print ("WINNER:" + str(connectFour.checkWinner(board)))
    if connectFour.checkWinner(board) == 1:
        w+=1
    elif connectFour.checkWinner(board) == 0:
        t+=1
    else:
        l+=1
print("WINS: %d  TIES: %d  LOSS: %d"%(w,t,l))

w = 0
t = 0
l = 0
for k in range(20):
    board = np.zeros((6,7))
    net40 = pop40.population[random.randint(0,19)]
    net0 = pop0.population[random.randint(0,19)]
    while(connectFour.checkWinner(board) ==2):
        move = 1#input("make a move: ")
        if not connectFour.check_valid(board, move):
            continue
        connectFour.play(board, 1, minimax.pickMove(board, 1, 3, net0))
        # connectFour.play(board, 1, move)
        #connectFour.print_board(board)
        # raw_input("press")
        #print
        if not connectFour.checkWinner(board)==2:
            break
        connectFour.play(board, -1, minimax.pickMove(board, -1, 3, net40))
        #connectFour.print_board(board)
    print ("WINNER:" + str(connectFour.checkWinner(board)))
    if connectFour.checkWinner(board) == -1:
        w+=1
    elif connectFour.checkWinner(board) == 0:
        t+=1
    else:
        l+=1
print("WINS: %d  TIES: %d  LOSS: %d"%(w,t,l))
#
# while True:
#     board = np.zeros((6,7))
#     while(connectFour.checkWinner(board) ==2):
#         move = input("make a move: ")
#         if not connectFour.check_valid(board, move):
#             continue
#         connectFour.play(board, 1, minimax.pickMove(board, 1, 3, net0))
#         # connectFour.play(board, 1, move)
#         connectFour.print_board(board)
#         # raw_input("press")
#         print
#         if not connectFour.checkWinner(board)==2:
#             break
#         connectFour.play(board, -1, minimax.pickMove(board, -1, 3, net40))
#         connectFour.print_board(board)
#     print ("WINNER:" + str(connectFour.checkWinner(board)))
