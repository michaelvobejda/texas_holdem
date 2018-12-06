###### Q-LEARNING #######################################
#########################################################

from mdp import PokerMDP
from collections import defaultdict

import random
#### DECLARE GLOBAL VARIABLES HERE #################################

max_iterations = 10
learning_rate = 0.8
discount = 1
weights = defaultdict(float)
explorationProb = 0.15
numRounds = 10

#### Q-LEARNING HELPER FUNCTIONS #################################

# Simplify board state to just consider board hands and player hand
def featureExtractor(state, action):
	return (sorted(state.board + state.players[state.curPlayer][0]), action)




#### Q-LEARNING MAIN FUNCTIONS #################################

# Return the Q function associated with the weights and features
def getQ(state, action):
	key = featureExtractor(state, action)
	return weights[keys]
    
# This algorithm will produce an action given a state 
# by following some strategy. 
# For example, we could use epsilon-greedy algorithm: 
# with probability |explorationProb|, take a random action.
def chooseAction(state, actions):
	if random.random() < explorationProb:
		return random.choice(actions)
	else:
		max_actions = []
		max_q = float('-inf')
		for a in actions:
			q = getQ(state, a)
			if (q > max_q):
				max_q = q
				max_actions = [a]
			elif (q == max_q):
				max_actions.append(a)
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

def simulateQLearning(playerWallets): 
	mdp = PokerMDP()
	state = mdp.initState()
	total_rewards = 0
	actions = mdp.getActions(state)
	for i in range(max_iterations):

		#CASE: Game Over
		if mdp.isEnd(state): 
		    break 

		# Choose action based on Q and epsilon-greedy search strategy. 
        best_action = chooseAction(state, actions)

        # Observe newState and associated reward. 
        newState, reward = mdp.sampleNextState(state, best_action)
        total_rewards += reward

        # Update Q weights 
        actions = mdp.getActions(newState)
        incorporateFeedback(state, best_action, reward, newState, actions, mdp.isEnd(newState))

		# Update state		
		state = newState


	return total_rewards


def runGame():
	playerWallets = [1000 for _ in range(numPlayers)
 	for _ in range(numRounds):
		playerMoney += simulateQLearning()
		print('Player money after ' + i + ' round: ' + playerMoney + '.')



if __name__ == '__main__':
	runGame()





