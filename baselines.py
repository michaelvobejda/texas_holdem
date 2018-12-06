###### BASELINES #######################################
#########################################################

from mdp import PokerMDP

agentQ = 0
num_trials = 5


#### GET_ACTIONS() METHODS #################################

def getRandomAction()

#### SIMULATION METHOD #################################

def simulate(actionCommand, numPlayers, maxRaise, playerWallets, trial_num):
	mdp = PokerMDP(numPlayers, maxRaise)
	state = mdp.initState()
	total_reward = 0
	its = 0
	while True:
		
		if mdp.isEnd(state): break

		curPlayer = state.curPlayer

		actions = mdp.getActions(state)

		# If player isn't agentQ, pick a random action. 
		if curPlayer != agentQ:
			action = getRandomAction(state, actions)
			newState, reward = mdp.sampleNextState(state, action)
			playerWallets[curPlayer] += reward
			state = newState
		# If player is agentQ, run standard find-action-that-maximizes-reward without lookahead. 
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
			playerWallets[curPlayer] += reward
			its += 1

	if its == 0:
		print "TRIAL:", trial_num, '- SIMULATION ITERATIONS EQUALS ZERO'
	else:
		print "TRIAL:", trial_num, " ", playerWallets		#DIVIDE PLAYERWALLETS VALUES BY ITS? 


#### CALL BASELINES #################################


def runBaselines(numPlayers, maxRaise, playerWallets):

	for i in range()



