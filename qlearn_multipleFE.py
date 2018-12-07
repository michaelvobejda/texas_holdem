###### Q-LEARNING #######################################
#########################################################

from mdp import PokerMDP
from collections import defaultdict
from deuces import Evaluator

import random

#### DECLARE GLOBAL VARIABLES HERE #################################

learning_rate = 1
discount = 1
explorationProb = 0.15

#HARD CODED FOR 5 PLAYERS
weights0 = defaultdict(float)
weights1 = defaultdict(float)
weights2 = defaultdict(float)
weights3 = defaultdict(float)
weights4 = defaultdict(float)

evaluator = Evaluator()

####Q learning feature extractors###
def standardFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, action)
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)

def actionAgnosticFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, )
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])))

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
		return evaluator.evaluate(state['board'][:5], hand)

def handRankAndBinaryFE(state, action):
	a = binaryActionFE(state, action)[1]
	hand = state['players'][state['curPlayer']][0]
	if not hand:
		return 0
	if len(state['board']) == 0:
		return (tuple(hand), a)
	else:
		return (evaluator.evaluate(state['board'][:5], hand), a)

####################################


#### Q-LEARNING MAIN FUNCTIONS #################################

# HARD-CODED!! Return the Q function associated with the weights and features
def getQ(state, action, curPlayer):
	if (curPlayer == 0):
		key = standardFE(state, action)
		return weights0[key]
	elif (curPlayer == 1):
		key = actionAgnosticFE(state, action)
		return weights1[key]
	elif (curPlayer == 2):
		key = binaryActionFE(state, action)
		return weights2[key]
	elif (curPlayer == 3):
		key = handRankFE(state, action)
		return weights3[key]
	else: 
		key = handRankAndBinaryFE(state, action)
		return weights4[key]	
    
# This algorithm will produce an action given a state 
# by following some strategy. 
# For example, we could use epsilon-greedy algorithm: 
# with probability |explorationProb|, take a random action.
def chooseAction(state, actions, curPlayer):
	if random.random() < explorationProb:
		return random.choice(actions)
	else:
		max_actions = [-1]
		max_q = float('-inf')
		for a in actions:
			q = getQ(state, a, curPlayer)
			#if (q!=0): print(q)
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
def incorporateFeedback(state, action, reward, newState, actions, newState_is_end, curPlayer):
	qp = 0
	if not newState_is_end:
		for a in actions:
			q = getQ(newState, a, curPlayer)
			if (q > qp):
				qp = q

	#update = learning_rate * (reward + (discount * qp) - getQ(state, action))
	if (action == -1): update = 0  
	else: 
		if (reward < 0):
			update = learning_rate * (abs(1/(reward+0.01)) + (discount * qp) - getQ(state, action, curPlayer))
		else: 
			update = learning_rate * (reward + (discount * qp) - getQ(state, action, curPlayer))
	
	if (curPlayer == 0):
		weights0[standardFE(state, action)] += update
	elif (curPlayer == 1):
		weights1[actionAgnosticFE(state, action)] += update
	elif (curPlayer == 2):
		weights2[binaryActionFE(state, action)] += update
	elif (curPlayer == 3):
		weights3[handRankFE(state, action)] += update
	elif (curPlayer == 4): 
		weights4[handRankAndBinaryFE(state, action)] += update



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

		# Choose action based on Q and epsilon-greedy search strategy. 
		if (curPlayer < 5):
			action = chooseAction(state, actions, curPlayer)
		else: 
			if (curPlayer == 5):
				action = random.choice(actions)
			elif (curPlayer == 6): 
				action = state['curBet'] - state['players'][state['curPlayer']][1]

        # Observe newState and associated reward. 
		newState, rewards = mdp.sampleNextState(state, action)
		reward = rewards[curPlayer]
		playerWallets[curPlayer] += reward

		# Get actions for new state
		actions = mdp.getActions(newState)		

        # Update Q weights 
		if curPlayer < 5:
			incorporateFeedback(state, action, reward, newState, actions, mdp.isEnd(newState), curPlayer)

		# Update state		
		state = newState
	return [len(weights0.keys()), len(weights1.keys()), len(weights2.keys()), len(weights3.keys()), len(weights4.keys())]










