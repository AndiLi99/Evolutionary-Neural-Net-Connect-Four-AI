import connectFour
import numpy as np
from copy import deepcopy
import random
import sys
import timer

#wrapper function to decide most promising move
def pickMove (board, player, depth, network):
    validMoves = []
    for i in range(7):
        if connectFour.check_valid(board, i):
            validMoves.append(i)

    scores = []

    for i in validMoves:
        scores.append(alphabeta(connectFour.play(deepcopy(board), player, i), depth -1, -1*(sys.maxint - 50), (sys.maxint - 50),player, -1*player, network))

    return validMoves[scores.index(max(scores))]

def alphabeta (node, depth, alpha, beta, player, currPlayer, network):
    win = connectFour.checkWinner(node)
    if not win == 2:
        return win*(sys.maxint - 50 + depth)*player
    if depth <= 0:
        v = network.feed_forward(node)
        if player == 1:
            return v[0]
        else:
            return v[1]
        # return random.random()

    validMoves = []

    for i in range(7):
        if connectFour.check_valid(node, i):
            validMoves.append(i)
    random.shuffle(validMoves)

    if player == currPlayer:
        v = -1*(sys.maxint - 50)
        for i in validMoves:
            v = max(v, alphabeta(connectFour.play(node, currPlayer, i), depth-1, alpha, beta, player, -1*currPlayer, network))
            connectFour.unplay(node, i)
            alpha = max(alpha, v)
            if beta <=  alpha:
                break #beta cutoff
        return v

    elif not player == currPlayer:
        v = 1*(sys.maxint - 50)
        for i in validMoves:
            v = min (v, alphabeta(connectFour.play(node, currPlayer, i), depth-1, alpha, beta, player, -1*currPlayer, network))
            connectFour.unplay(node, i)
            beta = min(beta, v)
            if beta <=  alpha:
                break #alpha cutoff
        return v
