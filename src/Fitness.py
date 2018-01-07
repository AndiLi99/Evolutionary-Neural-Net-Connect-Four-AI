import numpy as np
from random import randint
import net
from connectFour
import minimax

length = 7
height = 6

def compete(net1, net2):
    board = np.zeros((6,7))
    while(connectFour.checkWinner(board) ==2):
        connectFour.play(board, 1, minimax.pickMove(board, 1, 2, net1))
        if not connectFour.checkWinner(board) ==2:
            break
        connectFour.play(board, -1, minimax.pickMove(board, -1, 2, net2))

    return connectFour.checkWinner(board)

def populationFitness(population, numGamesPerIndividual):
    fitness = np.zeros(len(population))
    for x in range(len(population)):
        for y in range(numGamesPerIndividual):
            opponent = randint(0, len(population)-1)
            while opponent == x:
                opponent = randint(0, len(population)-1)
            winner = compete(population[x], population[opponent])
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
