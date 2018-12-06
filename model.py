from qlearn import simulateQLearning
import baselines as bs

# Global variables
numRounds = 10
agentQ = 0
numPlayers = 3
maxRaise = 50

def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNING
    for _ in range(numRounds):
        playerWallets = simulateQLearning(numPlayers, maxRaise, playerWallets)
        print('Player wallets after round ' + i + ': ' + playerMoney + '.')



if __name__ == '__main__':
    runGame()
