###### BASELINES #######################################
#########################################################

from mdp import PokerMDP
import random
import copy

agentQ = 0
num_trials = 5

debug = False

#### GET_ACTIONS() METHODS #################################

def foldEverytime(state, action):
	return -1

def getRandomAction(state, actions):
	return random.choice(actions)

def getMaxBetAction(state, actions):
	return max(actions)

#### SIMULATION METHOD #################################

def simulate(actionCommand, numPlayers, maxRaise, playerWallets, trial_num):
	mdp = PokerMDP(numPlayers, maxRaise)
	state = mdp.initState()
	while True:

		if debug:
			print('state:', state)
			print('player wallets:', playerWallets)

		if mdp.isEnd(state):
			rewards = mdp.getRewards(state, action)
			for i, reward in enumerate(rewards):
				playerWallets[i] += reward
			break

		curPlayer = state['curPlayer']
		actions = mdp.getActions(state)

		# If player isn't agentQ, pick a random action. 
		if curPlayer != agentQ:
			action = getRandomAction(state, actions)

		# If player is agentQ, run standard find-action-that-maximizes-reward without lookahead.
		# Player takes action according to specified actionCommand (different for each baseline!) 
		else: 
			action = actionCommand(state, actions)

		newState, rewards = mdp.sampleNextState(state, action)
		state = newState
		for i, reward in enumerate(rewards):
			playerWallets[i] += reward

		if debug:
			print('action:', action)
			print('rewards:', rewards)
			


	print "TRIAL:", trial_num, " ", playerWallets		#DIVIDE PLAYERWALLETS VALUES BY ITS? 


#### CALL BASELINES #################################

def runBaselines(numPlayers, maxRaise, playerWallets):

	# RANDOM ACTION POLICY
	print("RANDOM ACTION POLICY")
	for i in range(num_trials):
		actionCommand = getRandomAction
		simulate(actionCommand, numPlayers, maxRaise, copy.copy(playerWallets), i+1)

	# FOLD EVERYTIME
	print("FOLD EVERYTIME")
	for i in range(num_trials):
		actionCommand = foldEverytime
		simulate(actionCommand, numPlayers, maxRaise, copy.copy(playerWallets), i+1)

	# MAX ACTION UNIFORM POLICY
	print("MAX ACTION POLICY")
	for i in range(num_trials):
		actionCommand = getMaxBetAction
		simulate(actionCommand, numPlayers, maxRaise, copy.copy(playerWallets), i+1)



