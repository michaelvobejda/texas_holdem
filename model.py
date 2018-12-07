import qlearn 		#import simulateQLearning
#import qlearn_multipleFE as qlearn
import montecarlo
import baselines as bs
import copy
from collections import defaultdict
import matplotlib.pyplot as plt

# Global variables
numGames = 300000
numPlayers = 5
maxRaise = 50


def plotGraph(x, y):
    for i in range(numPlayers):
		if (i == qlearn.agentQ): l = "Agent Q (Agent " + str(i) + ")" 
		else: l = "Agent " + str(i)
		# if (i == 0): l = "Standard"
		# if (i == 1): l = "Action Agnostic"
		# if (i == 2): l = "Binary Action"
		# if (i == 3): l = "Hand Rank"
		# if (i == 4): l = "Hand Rank with Binary Action"
		# plt.plot(x, y[i], label=l)
		plt.plot(x, y[i], label=l)
    plt.xlabel('Simulations')
    plt.ylabel('Earnings')
    plt.title('Q-Learning with Standard Feature Extractor vs. Random-Policy Agents')
    plt.legend()
    plt.show()

def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNIG
    x = []
    y = defaultdict(list)
    for i in range(numGames):
        # qlearn.simulateQLearning(numPlayers, maxRaise, playerWallets)
        montecarlo.simulateMonteCarlo(numPlayers, maxRaise, playerWallets)
        if i % 10000 == 0:
    		print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')
    		x.append(i)
    		for j, monies in enumerate(playerWallets):
    			y[j].append(monies)
    plotGraph(x, y)



if __name__ == '__main__':
    runGame()
