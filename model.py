from qlearn import simulateQLearning
import baselines as bs

# Global variables
numGames = 10
agentQ = 0
numPlayers = 3
maxRaise = 50

def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNING
    for _ in range(numGames):
        playerWallets = simulateQLearning(numPlayers, maxRaise, playerWallets)
        print('Player wallets after game ' + i + ': ' + playerMoney + '.')



if __name__ == '__main__':
    runGame()
