import numpy as np
from random import randint
import connectFour
import timer
import minimax

length = 7
height = 6

def compete(net1, net2, print_board=False):
    board = np.zeros((6,7))
    while(connectFour.checkWinner(board) ==2):
        connectFour.play(board, 1, minimax.pickMove(board, 1, 2, net1))
        if print_board:
            connectFour.print_board(board)
        if not connectFour.checkWinner(board) ==2:
            break
        connectFour.play(board, -1, minimax.pickMove(board, -1, 2, net2))
        if print_board:
            connectFour.print_board(board)

    return connectFour.checkWinner(board)

def populationFitness(population, numGamesPerIndividual):
    fitness = np.zeros(len(population))
    for x in range(len(population)):
        print("Individual: " + str(x))
        for y in range(numGamesPerIndividual):
            opponent = randint(0, len(population)-1)
            while opponent == x:
                opponent = randint(0, len(population)-1)
            time = timer.Timer()
            winner = compete(population[x], population[opponent])
            time.lap()
            fitness[x] += winner
            fitness[opponent] -= winner
    return fitness

def getFittest(population, fitness_scores):
    max = fitness_scores[0]
    ind = 0
    for x in range(len(fitness_scores)):
        if fitness_scores[x] > max:
            max = fitness_scores[x]
            ind = x
    return population[ind]
