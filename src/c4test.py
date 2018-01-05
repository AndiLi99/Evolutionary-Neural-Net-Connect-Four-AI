import connectFour
import net
import sys
import Fitness
def pickMove(network, player, game):
    score = []
    for i in range(7):
        if game.check_valid(i):
                score.append(network.feed_forward_wrapper(Fitness.convertToPlayerBoard(game.newState(player, i).ravel(),player)))
        else:
            score.append(-9999999999)
    print score
    return score.index(max(score))

game = connectFour.Game()
network = net.load("c42.txt")
game.print_board()
while(game.checkWinner() == -1):
    move = input("Pick a move: ")
    # game.playPos(pickMove(network, 1, game))
    game.playPos(move)
    print
    if not game.checkWinner() == -1:
        break
    game.playPos(pickMove(network, 2, game))
print "The winner is: "
print game.checkWinner()
