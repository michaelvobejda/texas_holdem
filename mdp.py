###### MDP CLASS AND METHODS ############################
#########################################################

import math, random, itertools
from collections import defaultdict

class EpidemicMDP:

	#################################################################################
	#								GET ACTIONS 									#
	#################################################################################

	# Given a  state, returns all possible actions. 
	def getActions(self, state):


	#################################################################################
	#							GET NEXT STATE, ACTION & REWARD 					#
	#################################################################################

	# Checks to see if a state is a terminal state. 
	def isEnd(self, state):
		

	# Return reward for a given state
	def getReward(self, state): 


	# Generates a next state probabilistically based on current state. 
	def sampleNextState(self, state, action):

	#################################################################################
	#								INITIALIZE MDP 									#
	#################################################################################

	# builds initial state 
	def initState(self):

		return state


	def __init__(self):
		#DECLARE GLOBAL VARIABLES (HYPERPARAMETERS) HERE!
		self.state = self.initState()
