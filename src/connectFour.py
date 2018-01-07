import numpy as np
import copy
import net
import sys

def print_board(board):
    for i in reversed(range(6)):
        for x in range(7):
            if board[i][x] == 0:
                sys.stdout.write(". ")
            elif board[i][x] == 1:
                sys.stdout.write("X ")
            elif board[i][x] == -1:
                sys.stdout.write("O ")
            sys.stdout.flush()
        print
    print

def play (board, player, position):
    for y in range(6):
        if board[y][position] == 0:
            board[y][position] = player
            break
        elif y == 6:
            print "Error: invalid move"
    return board

def unplay (board, position):
    for y in reversed(range(6)):
        if not board[y][position] == 0:
            board[y][position] = 0
            break

def newState (board, player, position):
    g = copy.copy(board)
    for y in range(6):
        if g[y][position] == 0:
            g[y][position] = player
            break
    return g

def check_valid (board, position):
    for x in range(6):
        if board[x][position] == 0:
            return True
    return False

def checkWinner (board):
    for x in range (7):
        for y in range(6):
            playerID = board[y][x]

            if playerID == 0: continue

            if (x + 3 < 7):
                if (board[y][x+1] == playerID and
                            board[y][x+2] == playerID and
                            board[y][x+3] == playerID):
                    return playerID


            if (y + 3 < 6):
                if (board[y + 1][x] == playerID and
                            board[y + 2][x] == playerID and
                            board[y + 3][x] == playerID):
                    return playerID


            if (y + 3 < 6 and x + 3 < 7):
                if (board[y + 1][x + 1] == playerID and
                            board[y + 2][x + 2] == playerID and
                            board[y + 3][x + 3] == playerID):
                    return playerID


            if (y + 3 < 6 and x > 2):
                  if (board[y + 1][x - 1] == playerID and
                        board[y + 2][x - 2] == playerID and
                        board[y + 3][x - 3] == playerID):
                    return playerID


   #check for tie
    count = 0;
    for x in range(7):
        for y in range(6):
            if board[y][x] == 0:
                count+=1
    #tie
    if (count == 0):
        return 0
    #unfinished
    return 2
