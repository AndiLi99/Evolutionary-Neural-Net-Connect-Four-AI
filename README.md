# Connect-Four-Genetic-Algorithm
A genetic algorithm is used to evolve a population of convolutional neural networks. Each CNN is an individual, whose weights and biases for filters are coded as genes. The fitness of each member is evaluated by self-play against a global population of networks. Individuals who have a high fitness are selected to survive to the next generation, and able to breed. Breeding is done by combining parts of the feature map from the mother and father, a process inspired by crossover in genetics. Furthermore random mutations occur to randomly change a weight or bias by a random amount.

The CNN's take the input of the 6x7 space of the connect four board, and output using a softmax layer the predicted probabilities each player will win from that given position. During self-play, a minimax algorithm with alphabeta optimization is employed while selecting moves in order to stabilize learning. At the leaf nodes the CNN is used to evaluate board positions when the game does not have a winner. This process was inspired by Google's AlphaZero.

# Results
The machine plays very well against humans, winning on average ~95% of games. Analyzing the winrate of each generation against generation 0 results in some very interesting insights.

The generations immediately following generation 0 have an average winrate of 70%, which drops sharply and continues to fluctuate wildly. At about generation 60 the average winrate is slightly above 50%, which levels off to below 50% at generation 80 and beyond.

Continuing on, we hope to be able to have the networks learn more fluidly, with less fluctuations in winrate. The difficulty arises from the lack of training set, as there is no "right answer" to each board, without a previous databse of moves. 
