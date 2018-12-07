import qlearn 		#import simulateQLearning
import montecarlo
import baselines as bs
import copy
from collections import defaultdict

# Global variables
numGames = 100000000
numPlayers = 7
maxRaise = 50


def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNIG
    for i in range(numGames):
        # qlearn.simulateQLearning(numPlayers, maxRaise, playerWallets)
        montecarlo.simulateMonteCarlo(numPlayers, maxRaise, playerWallets)
        if i % 1 == 0:
        	# print(len(qlearn.weights))
            # print(len(montecarlo.weights))
            print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')



if __name__ == '__main__':
    runGame()
