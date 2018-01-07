import net
import connectFour
import numpy as np
from copy import deepcopy
import random
import sys

#wrapper function to decide most promising move
def pickMove (board, player, depth, network):
    validMoves = []
    for i in range(7):
        if connectFour.check_valid(board, i):
            validMoves.append(i)

    scores = []
    for i in validMoves:
        scores.append(alphabeta(connectFour.play(deepcopy(board), player, i), depth, -1*sys.maxint, sys.maxint,player, -1*player, network))

    print scores
    return validMoves[scores.index(max(scores))]

def alphabeta (node, depth, alpha, beta, player, currPlayer, network):
    win = connectFour.checkWinner(node)
    if not win == 2:
        print "winner is: " + str(win)
        return win*sys.maxint*player
    if depth == 0:
        # return network.feed_forward(node.gameState)
        b = random.random()
        return b

    validMoves = []

    for i in range(7):
        if connectFour.check_valid(node, i):
            validMoves.append(i)
    random.shuffle(validMoves)

    if player == currPlayer:
        print "my tun"
        v = -1*sys.maxint
        for i in validMoves:
            v = max(v, alphabeta(connectFour.play(deepcopy(node), currPlayer, i), depth-1, alpha, beta, player, -1*currPlayer, network))
            alpha = max(alpha, v)
            if beta <=  alpha:
                break #beta cutoff
        return v

    elif not player == currPlayer:
        v = 1*sys.maxint
        for i in validMoves:
            v = min (v, alphabeta(connectFour.play(deepcopy(node), currPlayer, i), depth-1, alpha, beta, player, -1*currPlayer, network))
            beta = min(beta, v)
            if beta <=  alpha:
                break #alpha cutoff
        return v

board = np.zeros((6,7))

print deepcopy(board)[0][0]
network = 0
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
    connectFour.play(board, -1, pickMove(board, -1, 3, 0))
    connectFour.print_board(board)
