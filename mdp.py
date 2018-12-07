###### MDP CLASS AND METHODS ############################
#########################################################

import math, random, itertools
from collections import defaultdict
from deuces import Deck, Evaluator, Card
import copy

evaluator = Evaluator()


class PokerMDP:

	#################################################################################
	#								    GET ACTIONS 								#
	#################################################################################

	# Given a  state, returns all possible actions. 
	def getActions(self, state):
		playerHand, playerBet = state['players'][state['curPlayer']]

		if not playerHand:
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
		return len(state['board']) == self.boardLength+1 or numFolded == self.numPlayers - 1


	def getWinner(self, state):
		if (self.isEnd(state)):
			numFolded = sum([1 if not player[0] else 0 for player in state['players']])
			if numFolded == self.numPlayers - 1:
				for i, player in enumerate(state['players']):
					if player[0]:
						return i

		
		#Return index of winner 
		best_rank = float("inf")
		index_of_best = 0
		for i, player in enumerate(state['players']):
			hand = player[0]
			if (hand):
				if len(state['board']) == 6:
					state['board'].pop(5)
				# print('board:')
				# Card.print_pretty_cards(state['board'])
				# print('hand:')
				# Card.print_pretty_cards(hand)
				rank = evaluator.evaluate(state['board'], hand)
				# print("Rank: ", rank)
				if (rank < best_rank): 
					best_rank = rank
					index_of_best = i
		
		return index_of_best


	# Return reward for a given state
	def getRewards(self, state, action):
		rewards = [0 for _ in range(self.numPlayers)]
		playerHand, playerBet = state['players'][state['curPlayer']]

		if self.isEnd(state):
			winner = self.getWinner(state)
			# print('Winner: ', winner)
			rewards[winner] += state['pot']
			return rewards

		if action == -1:
			return rewards

		rewards[state['curPlayer']] -= action
		return rewards



	#The round is over once all players have paid, which we know is true if the current player's bet is equal to the current bet
	def roundIsOver(self, state):
		#Unpack player state
		playerHand, playerBet = state['players'][state['curPlayer']]

		#Check if current player has folded
		if not playerHand:
			return False

		nextPlayer = (state['curPlayer'] + 1) % self.numPlayers
		nextPlayerHand, nextPlayerBet = state['players'][nextPlayer]
		roundOver = nextPlayerBet == state['curBet']
		# if roundOver:
			# print('\n\n!!!!!!!!!!!!!!!Round finished!!!!!!!!!!!!!!!!!:', state)
		return roundOver

	def getStartingPlayer(self, state):
		return random.choice([i for i in range(0, self.numPlayers)])
		# l = len(state['board'])
		# #Initial round of betting
		# if l == 0:
		# 	return 0
		# #Flop
		# if l == 3: 
		# 	return 1
		# #Turn
		# if l == 4:
		# 	return 2
		# #End of round				
		# if l == 5:
		# 	return 0 # HARDCODED FOR 3 PLAYERS
		# # End of game
		# if l == 6:
		# 	return 1

	# Generates a next state probabilistically based on current state
	def sampleNextState(self, state, action):

		# if generate:
			# deck = copy.copy(self.deck.cards)
		# else:
		deck = self.deck

		#Update state based on action
		rewards = self.getRewards(state, action)
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

		if self.roundIsOver(state):
			
			if len(state['board']) == 0:
				#Flop
				state['board'] = state['board'] + deck.draw(3)
			else:
				# print(len(state['board']))
				#Turn or River or End of round
				state['board'] = state['board'] + [deck.draw(1)]
			#Reset current bet for the round
			state['curBet'] = 0
			#Rotate starting bet
			state['curPlayer'] = self.getStartingPlayer(state)

			# Reset player bets for all players
			for i, player in enumerate(state['players']):
				state['players'][i] = (state['players'][i][0], False)
		else:
			state['curPlayer'] += 1
			state['curPlayer'] %= self.numPlayers

		return state, rewards

	#################################################################################
	#								INITIALIZE MDP 									#
	#################################################################################

	# builds initial state 
	def initState(self):
		state = {}
		state['board'] = []
		state['pot'] = 0
		state['curBet'] = 0
		#state['curPlayer'] = 0
		state['curPlayer'] = random.choice([i for i in range(0, self.numPlayers)])
		#player = (hand, curBet), hand=False if player has folded
		state['players'] = [(self.deck.draw(2), False) for _ in range(self.numPlayers)]
		
		return state


	def __init__(self, numPlayers, maxRaise, deck=False):
		self.numPlayers = numPlayers
		self.maxRaise = maxRaise + 1
		if deck:
			self.deck = deck
		else:
			self.deck = Deck()
		self.boardLength = 5

		#DECLARE GLOBAL VARIABLES (HYPERPARAMETERS) HERE!
