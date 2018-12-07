###### BASELINES #######################################
#########################################################

from mdp import PokerMDP
import random 

agentQ = 0
num_trials = 5


#### GET_ACTIONS() METHODS #################################

def getRandomAction(state, actions):
	if (actions == []): return [[]]
	return [random.choice(actions)]

def getMaxBetAction(state, actions):
	return [max(actions)]

#### SIMULATION METHOD #################################

def simulate(actionCommand, numPlayers, maxRaise, playerWallets, trial_num):
	mdp = PokerMDP(numPlayers, maxRaise)
	state = mdp.initState()
	total_reward = 0
	its = 0
	while True:
		
		if mdp.isEnd(state): 
			break

		curPlayer = state['curPlayer']

		actions = mdp.getActions(state)

		# If player isn't agentQ, pick a random action. 
		if curPlayer != agentQ:
			action = getRandomAction(state, actions)[0]
			newState, reward = mdp.sampleNextState(state, action)
			playerWallets[curPlayer] += reward
			state = newState

		# If player is agentQ, run standard find-action-that-maximizes-reward without lookahead.
		# Player takes action according to specified actionCommand (different for each baseline!) 
		else: 
			actions = actionCommand(state, actions)
			max_reward = float("-inf")
			max_state = state
			for action in actions: 
				newState, reward = mdp.sampleNextState(state, action)
				if (reward > max_reward):
					max_reward = reward
					max_state = newState
			state = max_state
			total_reward += max_reward
			playerWallets[curPlayer] += max_reward
			its += 1

	if its == 0:
		print "TRIAL:", trial_num, '- SIMULATION ITERATIONS EQUALS ZERO'
	else:
		print "TRIAL:", trial_num, " ", playerWallets		#DIVIDE PLAYERWALLETS VALUES BY ITS? 


#### CALL BASELINES #################################

def runBaselines(numPlayers, maxRaise, playerWallets):

	# RANDOM ACTION POLICY
	print("RANDOM ACTION POLICY")
	for i in range(num_trials):
		actionCommand = getRandomAction
		simulate(actionCommand, numPlayers, maxRaise, playerWallets, i+1)

	# MAX ACTION UNIFORM POLICY
	print("MAX ACTION POLICY")
	for i in range(num_trials):
		actionCommand = getMaxBetAction
		simulate(actionCommand, numPlayers, maxRaise, playerWallets, i+1)

	# BEST ACTION WITHOUT LOOKAHEAD 
	print("BEST ACTION WITHOUT LOOKAHEAD")
	for i in range(num_trials):
		actionCommand = callmdp.getActions
		simulate(actionCommand, numPlayers, maxRaise, playerWallets, i+1)





