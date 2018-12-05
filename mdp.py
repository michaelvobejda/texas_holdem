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

		if not playerHand:
			return []

		callVal = state.curBet - playerVet
		actions = range(call, call + self.maxRaise, 10)
		actions.append(-1)

		return actions


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


	#The round is over once all players have paid, which we know is true if the current player's bet is equal to the current bet
	def roundIsOver(state):
		#Unpack player state
		playerHand, playerBet = state.players[state.curPlayer]

		#Check if current player has folded
		if not playerHand:
			return False

		return playerBet == state.curBet

	def getStartingPlayer(state):
		l = len(state.board)
		#Initial round of betting
		if l == 0:
			return 0
		# Flop
		if l == 3: 
			return 1
		# Turn
		if l == 4:
			return 2
		# River
		if l == 5:
			return 3

	# Generates a next state probabilistically based on current state. 
	def sampleNextState(self, state, action):
		#Update state based on action
		if action == -1:
			state.players[state.curPlayer][0] = False
		else:
			state.curBet = action
			state.pot += curBet

		if roundIsOver(state):
			if  len(board) == 0:
				board += self.deck.draw(3)
			else:
				board += self.deck.draw(1)
			state.curBet = 0
			state.curPlayer = getStartingPlayer(state)
		else:
		
			state.curPlayer += 1
			state.curPlayer %= self.numPlayers

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


	def __init__(self):
		self.numPlayers = 4
		self.deck = Deck()
		self.maxRaise = 51
		#DECLARE GLOBAL VARIABLES (HYPERPARAMETERS) HERE!
		self.state = self.initState()
