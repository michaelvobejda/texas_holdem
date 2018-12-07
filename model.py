from qlearn import simulateQLearning
import baselines as bs
import copy

# Global variables
numGames = 10000000
agentQ = 0
numPlayers = 3
maxRaise = 50

####Q learning feature extractors###
def standardFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, action)
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)    

def actionAgnosticFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		# return (0, action)
		return 0
	# return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)
	return tuple(sorted(state['board'] + state['players'][state['curPlayer']][0]))

# def binaryActionFE(state, action):



####################################


def runGame():
    playerWallets = [1000 for _ in range(numPlayers)]
     
    #RUN BASELINES
    # bs.runBaselines(numPlayers, maxRaise, playerWallets)

    #RUN Q-LEARNING
    for i in range(numGames):
        simulateQLearning(numPlayers, maxRaise, playerWallets)
        if i % 10000 == 0:
            print('Player wallets after game ' + str(i) + ': ' + str(playerWallets) + '.')



if __name__ == '__main__':
    runGame()
