from qlearn import simulateQLearning


# Global variables
numRounds = 10
agentQ = 0
numPlayers = 3
maxRaise = 50

def runGame():
	playerWallets = [1000 for _ in range(numPlayers)]
 	for _ in range(numRounds):
		playerWallets = simulateQLearning(numPlayers, maxRaise, playerWallets)
		print('Player wallets after round ' + i + ': ' + playerMoney + '.')



if __name__ == '__main__':
	runGame()
