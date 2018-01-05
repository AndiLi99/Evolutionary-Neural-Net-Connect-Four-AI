import numpy as np
from random import randint
import net
from connectFour import Game

length = 7
height = 6

def getWinner (game):
    return game.checkWinner()

def play (game, player, position):
    return game.play(player, position)

def newgameState (game, player, position):
    return game.newState(player, position)

def convertToPlayerBoard (arr, playerNum):
    a = np.zeros(42)
    for x in range(42):
            if arr[x] == playerNum:
                a[x] = 1
            elif arr[x] == 0:
                a[x] = 0
            else:
                a[x] = -1
    return a
# Plays 2 networks against each other
# Returns 1 if net1 wins, -1 if net2 wins, 0 if draw
def compete (net1, net2):
    game = Game()
    game_end = False
    cnt = 0
    while not game_end:
        c_player = net1
        if cnt%2 == 1:
            c_player = net2
        scores = np.zeros(length)
        valid = [True for x in range(7)]
        for x in range(length):
            if game.check_valid(x):
                curr_state = newgameState(game, cnt%2+1, x).ravel()
                s = c_player.feed_forward(convertToPlayerBoard(curr_state, cnt%2+1))
                scores[x] = s[0]
            else:
                valid[x] = False
        max = -9999999999
        ind = -1
        for x in range(length):
            if scores[x] > max and valid[x]:
                max = scores[x]
                ind = x
        play(game, cnt%2+1, ind)
        cnt+=1
        if not game.checkWinner() == -1:
            game_end = True
    if getWinner(game) == 1:
        return 1
    elif getWinner(game) == 2:
        return -1
    return 0

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
