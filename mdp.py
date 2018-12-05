###### MDP CLASS AND METHODS ############################
#########################################################

import math, random, itertools
from collections import defaultdict
from deuces import Deck, Evaluator

class PokerMDP:

	#################################################################################
	#								GET ACTIONS 									#
	#################################################################################

	# Given a  state, returns all possible actions. 
	def getActions(self, state):
		playerHand, playerBet = state.players[state.curPlayer]
		callVal = state.curBet - playerVet
		RAISE = range(call, call + self.maxRaise, 10)
		RAISE.append(-1)

		return RAISE


	#################################################################################
	#							GET NEXT STATE, ACTION & REWARD 					#
	#################################################################################

	# Checks to see if a state is a terminal state. 
	def isEnd(self, state):
		folded = sum([1 if not player else 0 for player in state.players])
		return len(state.board) == 5 or folded == self.numPlayers - 1

	def getWinner(self, state):
		results = [Evaluator.evaluate(player[0]) for player in state.curPlayer]

		return results.index(max(results))

	# Return reward for a given state
	def getReward(self, state):
		playerHand, playerBet = state.players[state.curPlayer]

		if not playerHand:
			return 0
		if isEnd(state):
			winner = getWinner(state)
			if state.curPlayer == winner:
				return state.pot
			else:
				return 0
		else:
			return -1*playerBet


	# Generates a next state probabilistically based on current state. 
	def sampleNextState(self, state, action):

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
		state['players'] = [(self.deck.draw(2), 0) for _ in range(self.numPlayers)]

		return state


	def __init__(self):
		self.numPlayers = 4
		self.deck = Deck()
		self.maxRaise = 51
		#DECLARE GLOBAL VARIABLES (HYPERPARAMETERS) HERE!
		self.state = self.initState()
