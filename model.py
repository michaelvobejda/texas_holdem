# import qlearn 		#import simulateQLearning
import qlearn_multipleFE as qlearn
import montecarlo
import baselines as bs
import copy
from collections import defaultdict
import matplotlib.pyplot as plt

# Global variables
numGames = 1000000
numPlayers = 7
maxRaise = 50


def plotGraph(x, walletY, weightLenY):
    for i in range(numPlayers):
        if i == 0: 
            l = "Standard"
        if i == 1: 
            l = "Action Agnostic"
        if i == 2: 
            l = "Binary Action"
        if i == 3: 
            l = "Hand Rank"
        if i == 4: 
            l = "Hand Rank with Binary Action"
        if i == 5:
            l = "Random Action"
        if i == 6:
            l = "Always Call"

        plt.plot(x, walletY[i], label=l)
    plt.xlabel('Games Played')
    plt.ylabel('Earnings')
    plt.title('Earning of Q Agents Over Time')
    plt.legend()
    plt.show()

    for i in range(numPlayers - 1):
        if i == 0: 
            l = "Standard"
        if i == 1: 
            l = "Action Agnostic"
        if i == 2: 
            l = "Binary Action"
        if i == 3: 
            l = "Hand Rank"
        if i == 4: 
            l = "Hand Rank with Binary Action"
        if i == 5:
            l = "Random Action"

        plt.plot(x, walletY[i], label=l)
    plt.xlabel('Games Played')
    plt.ylabel('Earnings')
    plt.title('Earning of Q Agents Over Time')
    plt.legend()
    plt.show()

    for i in range(numPlayers - 2):

		if (i == 0): l = "Standard"
		if (i == 1): l = "Action Agnostic"
		if (i == 2): l = "Binary Action"
		if (i == 3): l = "Hand Rank"
		if (i == 4): l = "Hand Rank with Binary Action"
        
		plt.plot(x, weightLenY[i], label=l)
    plt.xlabel('Games Played')
    plt.ylabel('Number of elements in Q matrix')
    plt.title('Number of Unique Q Matrix Values Over Time')
    plt.legend()
    plt.show()

def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
        
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNING
    x = []
    walletY = [[] for _ in range(numPlayers)]
    weightLenY = [[] for _ in range(numPlayers)]
    for i in range(numGames):

        weightLens = qlearn.simulateQLearning(numPlayers, maxRaise, playerWallets)
        # montecarlo.simulateMonteCarlo(numPlayers, maxRaise, playerWallets)
        if i % 10000 == 0:
            print('~~~~~ GAME ' + str(i) + ' ~~~~~')
            print('weight lens:', weightLens)
            print('player wallets:', playerWallets)
            # print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')
            x.append(i)
            for i, weightLen in enumerate(weightLens):
                weightLenY[i].append(weightLen)
            for j, playerWallet in enumerate(playerWallets):
                walletY[j].append(playerWallet)
    plotGraph(x, walletY, weightLenY)



if __name__ == '__main__':
    runGame()
