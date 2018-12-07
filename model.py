import qlearn 		#import simulateQLearning
import baselines as bs
import copy
from collections import defaultdict

# Global variables
numGames = 10000000
numPlayers = 3
maxRaise = 50


def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNIG
    for i in range(numGames):
        qlearn.simulateQLearning(numPlayers, maxRaise, playerWallets)
        if i % 10000 == 0:
        	print(len(qlearn.weights))
    		print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')



if __name__ == '__main__':
    runGame()
