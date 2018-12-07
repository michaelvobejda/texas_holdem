###### MDP CLASS AND METHODS ############################
#########################################################

import math, random, itertools
from collections import defaultdict
from deuces import Deck, Evaluator

evaluator = Evaluator()


class PokerMDP:

	#################################################################################
	#								GET ACTIONS 									#
	#################################################################################

	# Given a  state, returns all possible actions. 
	def getActions(self, state):
		playerHand, playerBet = state['players'][state['curPlayer']]

		if not playerHand:
			#return []
			return [-1]

		callVal = state['curBet'] - playerBet
		actions = [a for a in range(callVal, callVal + self.maxRaise, 10)]
		actions.append(-1)

		return actions


	#################################################################################
	#							GET NEXT STATE, ACTION & REWARD 					#
	#################################################################################

	# Checks to see if a state is a terminal state. 
	def isEnd(self, state):
		numFolded = sum([1 if not player[0] else 0 for player in state['players']])
		return len(state['board']) == self.boardLength or numFolded == self.numPlayers - 1


	def getWinner(self, state):

		#SPECIAL CASE: All players fold in first round (when state['board'] == [])
		#In this case, the last player to have bet wins. 
		if (state['board'] == []):
			return self.numPlayers-1
		
		#Return index of winner 
		best_rank = float("inf")
		index_of_best = None
		for i, player in enumerate(state['players']):
			hand = player[0]
			if (hand != False): 
				rank = evaluator.evaluate(hand, state['board'])
				if (rank < best_rank): 
					best_rank = rank
					index_of_best = i
		
		return index_of_best
		#results = [evaluator.evaluate(state['board'], player[0]) for player in state['players']]
		#return results.index(min(results))


	# Return reward for a given state
	def getReward(self, state):
		# print('curPlayer:', state['curPlayer'])
		# print('len of players:', len(state['players']))
		playerHand, playerBet = state['players'][state['curPlayer']]

		if not playerHand:
			return 0
		if self.isEnd(state):
			winner = self.getWinner(state)
			if state['curPlayer'] == winner:
				return state['pot']
			else:
				return 0

		else:
			return -1*playerBet
			# if self.roundIsOver(state):
			# 	return -1*playerBet
			# else:
			# 	return 0


	#The round is over once all players have paid, which we know is true if the current player's bet is equal to the current bet
	def roundIsOver(self, state):
		#Unpack player state
		playerHand, playerBet = state['players'][state['curPlayer']]

		# #Check if current player has folded
		# if not playerHand:
		# 	return False

		#WARNING: Code below is hard-coded for self.boardLength = 5!! 
		start = self.getStartingPlayer(state)
		if (start == 0):
			return state['curPlayer'] == 2
		elif (start == 1):
			return state['curPlayer'] == 0
		else: 
			return state['curPlayer'] == 1

		#OLD: return playerBet == state['curBet']

	def getStartingPlayer(self, state):
		l = len(state['board'])
		#Initial round of betting
		if l == 0:
			return 0
		#Flop
		if l == 3: 
			return 1
		#Turn
		if l == 4:
			return 2
		#End of round				
		if l == 5:
			return 0

	# Generates a next state probabilistically based on current state
	def sampleNextState(self, state, action):
		#Update state based on action
		if action == -1:
			#Player folded, set their hand to False
			state['players'][state['curPlayer']] = (False, state['players'][state['curPlayer']][1])
		else:
			#Add players action to their running total bet
			if (state['players'][state['curPlayer']][1] == False): newPlayerBet = action   	#if current bet is False
			else: newPlayerBet = state['players'][state['curPlayer']][1] + action
			state['players'][state['curPlayer']] = (state['players'][state['curPlayer']][0], newPlayerBet)
			#Total bet for the round is equal to the player's total running bet
			state['curBet'] = newPlayerBet
			#Add the players bet to the pot
			state['pot'] += action

		if self.roundIsOver(state):
			if len(state['board']) == 0:
				#Flop
				state['board'] = state['board'] + self.deck.draw(3)
			else:
				#Turn or River or End of round
				state['board'] = state['board'] + [self.deck.draw(1)]
			#Reset current bet for the round
			state['curBet'] = 0
			#Rotate starting bet
			state['curPlayer'] = self.getStartingPlayer(state)
		else:
			state['curPlayer'] += 1
			state['curPlayer'] %= self.numPlayers

		return state, self.getReward(state)

	#################################################################################
	#								INITIALIZE MDP 									#
	#################################################################################

	# builds initial state 
	def initState(self):
		state = {}
		state['board'] = []
		state['pot'] = 0
		state['curBet'] = 0
		state['curPlayer'] = 0
		#player = (hand, curBet), hand=False if player has folded
		state['players'] = [(self.deck.draw(2), False) for _ in range(self.numPlayers)]
		
		return state


	def __init__(self, numPlayers, maxRaise):
		self.numPlayers = numPlayers
		self.maxRaise = maxRaise + 1
		self.deck = Deck()
		self.boardLength = 5

		#DECLARE GLOBAL VARIABLES (HYPERPARAMETERS) HERE!
