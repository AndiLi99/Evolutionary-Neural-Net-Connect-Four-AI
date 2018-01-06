import numpy as np
import copy
import net
class Game:
    def __init__(self):
        self.gameState = np.zeros((6, 7))
        self.lastPlayed = 1

    def print_board(self):
        for i in reversed(range(6)):
            print(self.gameState[i])

    def playPos (self, position):
        if self.check_valid(position):
            for y in range(6):
                if self.gameState[y][position] == 0:
                    self.gameState[y][position] = self.lastPlayed
                    self.lastPlayed+=1
                    if self.lastPlayed == 3:
                        self.lastPlayed = 1
                    break
        self.print_board()

    def play (self, player, position):
        for y in range(6):
            if self.gameState[y][position] == 0:
                self.gameState[y][position] = player
                break
            elif y == 6:
                return -1
        return 1

    def newState (self, player, position):
        g = copy.copy(self.gameState)
        for y in range(6):
            if g[y][position] == 0:
                g[y][position] = player
                break
        return g

    def check_valid (self, position):
        for x in range(6):
            if self.gameState[x][position] == 0:
                return True
        return False

    def checkWinner (self):
        arr = self.gameState
        for x in range (7):
            for y in range(6):
                playerID = self.gameState[y][x]

                if playerID == 0: continue

                if (x + 3 < 7):
                    if (self.gameState[y][x+1] == playerID and
                                self.gameState[y][x+2] == playerID and
                                self.gameState[y][x+3] == playerID):
                        return playerID


                if (y + 3 < 6):
                    if (self.gameState[y + 1][x] == playerID and
                                self.gameState[y + 2][x] == playerID and
                                self.gameState[y + 3][x] == playerID):
                        return playerID


                if (y + 3 < 6 and x + 3 < 7):
                    if (self.gameState[y + 1][x + 1] == playerID and
                                self.gameState[y + 2][x + 2] == playerID and
                                self.gameState[y + 3][x + 3] == playerID):
                        return playerID


                if (y + 3 < 6 and x > 2):
                      if (self.gameState[y + 1][x - 1] == playerID and
                            self.gameState[y + 2][x - 2] == playerID and
                            self.gameState[y + 3][x - 3] == playerID):
                        return playerID


       #check for tie
        count = 0;
        for x in range(7):
            for y in range(6):
                if self.gameState[y][x] == 0:
                    count+=1
        #tie
        if (count == 0):
            return 0
        #unfinished
        return -1
