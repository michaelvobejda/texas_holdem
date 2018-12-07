from qlearn import simulateQLearning
import baselines as bs
import copy

# Global variables
numGames = 10000000
agentQ = 0
numPlayers = 3
maxRaise = 50


def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNIG

    for i in range(numGames):
        simulateQLearning(numPlayers, maxRaise, playerWallets)
        if i % 10000 == 0:
            print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')



if __name__ == '__main__':
    runGame()
