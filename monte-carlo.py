from mdp import PokerMDP
from collections import defaultdict
import random
import math

max_iterations = 10
discount = 1
visited = []
counts = defaultdict(defaultdict(int))
weights = defaultdict(float)

mdp = PokerMDP()
cur_state = mdp.initState()


################### HELPER FUNCTIONS ###############################
# Simplify board state to just consider board hands and player hand
def featureExtractor(state, action):
	return (sorted(state.board + state.players[state.curPlayer][0]), action)

def setQ(state, action, val):
	key = featureExtractor(state)
	weights[key] = val


# Return the Q function associated with the weights and features
def getQ(state, action):
	key = featureExtractor(state, action)
	return weights[key]

#################### MAIN FUNCTIONS #################################
def simulate(state, depth):
	if depth == 0:
		return 0

	if state not in visited:
		visited.append(state)
		return rollout(state, depth)

	actions = mdp.getActions(state)
	max_actions = []
	max_val = float('-inf')
	for a in actions:
		Q = getQ(state, a)
		val = Q + c*math.sqrt(math.log(sum(counts[state]))/counts[state][a])
		if (val > max_val):
			max_val = val
			max_actions = [a]
		elif (val == max_val):
			max_actions.append(a)
	a = random.choice(max_actions)

	# Observe newState and associated reward. 
    newState, reward = mdp.sampleNextState(state, best_action)
    total_rewards += reward

    cur_state = newState

    q = reward + discount*simulate(newState, depth-1)
    counts[state][action] += 1

    Q = getQ(state, a)
    newQ = Q + (q-Q)/counts[state][action]
    setQ(state,action,newQ)

    return q

def rollout(state, depth):
	if depth == 0:
		return 0

	#set action to default policy
	a = mdp.getActions(state)[0]

	newState, reward = mdp.sampleNextState(state, best_action)

	return reward + discount*rollout(newState, depth-1)

def selectAction(state, depth):
	for i in range(max_iterations):
		simulate(state, actions, depth)

	best_actions = []
	max_q = float("-inf")
	for a in actions:
		q = getQ(state, a)
		if (q > max_q):
			max_q = q
			max_actions = [a]
		elif (q == max_q):
			max_actions.append(a)
	return random.choice(max_actions)


def runGame():
	playerWallets = [1000 for _ in range(numPlayers)
 	for _ in range(numRounds):
		playerMoney += simulate(cur_state, DEPTH)
		print('Player money after ' + i + ' round: ' + playerMoney + '.')



if __name__ == '__main__':
	runGame()