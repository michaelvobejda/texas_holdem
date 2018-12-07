###### Q-LEARNING #######################################
#########################################################

from mdp import PokerMDP
from collections import defaultdict
from deuces import Evaluator

import random
#### DECLARE GLOBAL VARIABLES HERE #################################


learning_rate = 0.8
discount = 1
weights = defaultdict(float)
explorationProb = 0.15
agentQ = 0

evaluator = Evaluator()

####Q learning feature extractors###
def standardFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, action)
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)

def actionAgnosticFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, )
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)

def binaryActionFE(state, action):
	if action == -1:
		a = 0
	else:
		a = 1
	if not state['players'][state['curPlayer']][0]:
		return (0, a)
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), a)

def handRankFE(state, action):
	hand = state['players'][state['curPlayer']][0]
	if not hand:
		return 0
	if len(state['board']) == 0:
		return tuple(hand)
	else:
		return evaluator.evaluate(state['board'], hand)

featureExtractor = binaryActionFE

####################################


#### Q-LEARNING MAIN FUNCTIONS #################################

# Return the Q function associated with the weights and features
def getQ(state, action):
	key = featureExtractor(state, action)
	return weights[key]
    
# This algorithm will produce an action given a state 
# by following some strategy. 
# For example, we could use epsilon-greedy algorithm: 
# with probability |explorationProb|, take a random action.
def chooseAction(state, actions):
	if random.random() < explorationProb:
		return random.choice(actions)
	else:
		max_actions = [-1]
		max_q = float('-inf')
		for a in actions:
			q = getQ(state, a)
			if (q > max_q):
				max_q = q
				max_actions = [a]
			elif (q == max_q):
				max_actions.append(a)
		# print('max actions:', max_actions)
		return random.choice(max_actions)


# Call this function with (s, a, r, s'), which you should use to update |weights|.
# Note that if s is a terminal state, then s' will be None.   
# Use getQ() to compute the current estimate of the parameters.
def incorporateFeedback(state, action, reward, newState, actions, newState_is_end):
	qp = 0
	if not newState_is_end:
		for a in actions:
			q = getQ(newState, a)
			if (q > qp):
				qp = q
		update = learning_rate * (reward + (discount * qp) - getQ(state, action))
		weights[featureExtractor(state, action)] += update


#### SIMULATE (RUN Q-LEARNING) #####################################

def simulateQLearning(numPlayers, maxRaise, playerWallets):
	mdp = PokerMDP(numPlayers, maxRaise)
	state = mdp.initState()
	actions = mdp.getActions(state)
	while True:

		#CASE: Game Over
		if mdp.isEnd(state): 
			rewards = mdp.getRewards(state, action)
			for i, reward in enumerate(rewards):
				playerWallets[i] += reward
			break 

		curPlayer = state['curPlayer']

		# If player is agentQ, choose action based on Q and epsilon-greedy search strategy. 
		if curPlayer == agentQ:
			action = chooseAction(state, actions)
		# Else select random action
		else:
			action = random.choice(actions) # TODO: write a better function

        # Observe newState and associated reward. 
		newState, rewards = mdp.sampleNextState(state, action)
		reward = rewards[curPlayer]
		playerWallets[curPlayer] += reward

		# Get actions for new state
		actions = mdp.getActions(newState)		

        # Update Q weights 
		if curPlayer == agentQ:
			incorporateFeedback(state, action, reward, newState, actions, mdp.isEnd(newState))

		# Update state		
		state = newState









