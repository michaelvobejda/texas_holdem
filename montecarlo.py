from mdp import PokerMDP
from collections import defaultdict
import random
import math
from deuces import Evaluator, Deck, Card
import copy

max_iterations = 10
discount = 1
visited = []
counts = defaultdict(lambda: defaultdict(int))
weights = defaultdict(float)
agentCarlo = 4
c = 1 # exploration constant

evaluator = Evaluator()

#### Feature Extractors ####
def standardFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, action)
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), action)

def actionAgnosticFE(state, action):
	if not state['players'][state['curPlayer']][0]:
		return (0, )
	return (tuple(sorted(state['board'] + state['players'][state['curPlayer']][0])), )

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
	if len(state['board']) < 5:
		return tuple(hand)
	else:
		if (len(state['board']) == 6): return evaluator.evaluate(state['board'][:5], hand)
		return evaluator.evaluate(state['board'], hand)

def handRankAndBinaryFE(state, action):
	a = binaryActionFE(state, action)[1]
	hand = state['players'][state['curPlayer']][0]
	if not hand:
		return 0
	if len(state['board']) < 5:
		return tuple(hand)
	else:
		if (len(state['board']) == 6): return (evaluator.evaluate(state['board'][:5], hand), a)
		return (evaluator.evaluate(state['board'], hand), a)


featureExtractor = handRankAndBinaryFE	


################### HELPER FUNCTIONS ###############################
def generate(mdp, state, action):
	cardsInUse = []
	for player in state['players']:
		hand = player[0]
		if not hand:
			continue
		for card in hand:
			cardsInUse.append(card)
	for card in state['board']:
		cardsInUse.append(card)

	fullDeck = Deck().GetFullDeck()
	deck = [card for card in fullDeck if card not in cardsInUse]

	random.shuffle(deck)

	#Update state based on action
	rewards = mdp.getRewards(state, action)
	if action == -1:
		#Player folded, set their hand to False
		state['players'][state['curPlayer']] = (False, state['players'][state['curPlayer']][1])
	else:
		#Add players action to their running total bet
		if (state['players'][state['curPlayer']][1] == False): 
			newPlayerBet = action   	#if current bet is False
		else: 
			newPlayerBet = state['players'][state['curPlayer']][1] + action
		state['players'][state['curPlayer']] = (state['players'][state['curPlayer']][0], newPlayerBet)
		#Total bet for the round is equal to the player's total running bet
		state['curBet'] = newPlayerBet
		#Add the players bet to the pot
		state['pot'] += action

	if mdp.roundIsOver(state):
		
		if len(state['board']) == 0:
			#Flop
			newcards = [deck.pop(0) for _ in range(3)]
			state['board'] = state['board'] + newcards
		else:
			#Turn or River or End of round
			state['board'] = state['board'] + [deck.pop(0)]
		#Reset current bet for the round
		state['curBet'] = 0
		#Rotate starting bet
		state['curPlayer'] = mdp.getStartingPlayer(state)

		# Reset player bets for all players
		for i, player in enumerate(state['players']):
			state['players'][i] = (state['players'][i][0], False)
	else:
		state['curPlayer'] += 1
		state['curPlayer'] %= mdp.numPlayers

	return state, rewards

# Simplify board state to just consider board hands and player hand
def setQ(state, action, val):
	key = featureExtractor(state, action)
	weights[key] = val


# Return the Q function associated with the weights and features
def getQ(state, action):
	key = featureExtractor(state, action)
	return weights[key]

#################### MAIN FUNCTIONS #################################
def simulate(mdp, state, depth):
	# generator = PokerMDP(mdp.numPlayers, mdp.maxRaise-1, copy.deepcopy(mdp.deck))

	if depth == 0:
		return 0

	actions = mdp.getActions(state)
	if state not in visited:
		visited.append(tuple(state))
		for action in actions:
			counts[tuple(state)][action] = 1

		return rollout(mdp, state, depth)

	max_actions = []
	max_val = float('-inf')
	for a in actions:
		Q = getQ(state, a)
		val = Q + c * math.sqrt(math.log(sum(counts[tuple(state)]))/counts[tuple(state)][a])
		if (val > max_val):
			max_val = val
			max_actions = [a]
		elif (val == max_val):
			max_actions.append(a)
	a = random.choice(max_actions)

	# Observe newState and associated reward. 
	# newState, rewards = generator.sampleNextState(state, a)
	newState, rewards = generate(mdp, state, a)
	reward = rewards[state['curPlayer']]

	cur_state = newState

	q = reward + discount*simulate(mdp, newState, depth-1)
	counts[state][action] += 1

	Q = getQ(state, a)
	newQ = Q + (q-Q)/counts[state][action]
	setQ(state, action, newQ)

	return q

def rollout(mdp, state, depth):
	if depth == 0:
		return 0

	# generator = PokerMDP(mdp.numPlayers, mdp.maxRaise-1, copy.deepcopy(mdp.deck))

	#set action to default policy, which is calling
	a = mdp.getActions(state)[0]
	# newState, rewards = generator.sampleNextState(state, a)
	newState, rewards = generate(mdp, state, a)
	reward = rewards[state['curPlayer']]

	return reward + discount*rollout(mdp, newState, depth-1)

def chooseAction(mdp, state, depth):
	for i in range(max_iterations):
		simulate(mdp, state, depth)

	best_actions = []
	max_q = float("-inf")
	actions = mdp.getActions(state)
	for a in actions:
		q = getQ(state, a)
		if (q > max_q):
			max_q = q
			max_actions = [a]
		elif (q == max_q):
			max_actions.append(a)
	return random.choice(max_actions)



def simulateMonteCarlo(numPlayers, maxRaise, playerWallets):
	mdp = PokerMDP(numPlayers, maxRaise)
	state = mdp.initState()
	actions = mdp.getActions(state)
	depth = 3
	while True:

		#CASE: Game Over
		if mdp.isEnd(state): 
			rewards = mdp.getRewards(state, action)
			for i, reward in enumerate(rewards):
				playerWallets[i] += reward
			break 

		curPlayer = state['curPlayer']

		# If player is agentQ, choose action based on Q and epsilon-greedy search strategy. 
		if curPlayer == agentCarlo:
			action = chooseAction(mdp, state, depth)
		# Else select random action
		else:
			# action = state['curBet'] - state['players'][state['curPlayer']][1]  
			action = random.choice(actions) # TODO: write a better function

        # Observe newState and associated reward. 
		newState, rewards = mdp.sampleNextState(state, action)
		reward = rewards[curPlayer]
		playerWallets[curPlayer] += reward

		# Get actions for new state
		actions = mdp.getActions(newState)		

        # Update Q weights 
		# if curPlayer == agentCarlo:
			# incorporateFeedback(state, action, reward, newState, actions, mdp.isEnd(newState))

		# Update state		
		state = newState

	return weights 
