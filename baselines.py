###### BASELINES #######################################
#########################################################

from mdp import PokerMDP

max_iterations = 50

#### GET_ACTIONS() METHODS #################################

def getRandomAction()

#### SIMULATION METHOD #################################

def simulate(actionCommand):
	grand_total_rewards = 0
	mdp = PokerMDP()
	s = mdp.initState()
	total_reward = 0
	its = 0
	for i in range(max_iterations):
		
		if mdp.isEnd(s): break

		actions = actionCommand(s)
		max_reward = float("-inf")
		max_state = s
		for action in actions: 
			new_s, reward = mdp.sampleNextState(s, action)
			if (reward > max_reward):
				max_reward = reward
				max_state = new_s
		s = max_state
		total_reward += max_reward
		its += 1

	if its == 0:
		print "TRIAL:", trial_num, '- SIMULATION ITERATIONS EQUALS ZERO'
	else:
		avg_reward = total_reward/float(its)
		#print "TRIAL:", trial_num, " ", avg_reward
		print avg_reward

#### CALL BASELINES #################################






