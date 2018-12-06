###### Q-LEARNING #######################################
#########################################################

from mdp import PokerMDP

#### DECLARE GLOBAL VARIABLES HERE #################################

max_iterations = 50
learning_rate = 0.8
discount = 1

#### Q-LEARNING HELPER FUNCTIONS #################################

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def featureExtractor(state, action):


# OPTIONAL
# Call this function to get the step size to update the weights.
def getStepSize(num_iterations):

#### Q-LEARNING MAIN FUNCTIONS #################################

# Return the Q function associated with the weights and features
def getQ(state, action):
	score = 0
    for f, v in featureExtractor(state, action):
        score += weights[f] * v
    #if (score != 0): print("SCORE: ", score)
    return score
    
# This algorithm will produce an action given a state 
# by following some strategy. 
# For example, we could use epsilon-greedy algorithm: 
# with probability |explorationProb|, take a random action.
def chooseAction(state, actions):

# Call this function with (s, a, r, s'), which you should use to update |weights|.
# Note that if s is a terminal state, then s' will be None.   
# Use getQ() to compute the current estimate of the parameters.
def incorporateFeedback(state, action, reward, newState, actions, num_iterations, newState_is_end):


#### SIMULATE (RUN Q-LEARNING) #####################################

def simulateQLearning(number_of_trials): 
	mdp = PokerMDP()
	state = mdp.state
	total_rewards = 0
	num_iterations = 0
	actions = mdp.getActions(state)
	for i in range(max_iterations):

		#CASE: Game Over
		if mdp.isEnd(state): 
		    break 

		# Choose action based on Q and epsilon-greedy search strategy. 
        best_action = chooseAction(state, actions)
        num_iterations += 1

        # Observe newState and associated reward. 
        newState, reward = mdp.sampleNextState(state, best_action)
        total_rewards += reward

        # Update Q weights 
        actions = mdp.getActions(newState)
        incorporateFeedback(state, best_action, reward, newState, actions, num_iterations, mdp.isEnd(newState))

	avg_reward = total_rewards/float(num_iterations)
 	print(avg_reward)






