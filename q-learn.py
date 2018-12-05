###### Q-LEARNING #######################################
#########################################################

from mdp import PokerMDP


#### DECLARE GLOBAL VARIABLES HERE #################################


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

	# avg_reward = total_rewards/float(num_iterations)
 	# print(avg_reward)