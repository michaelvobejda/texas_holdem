from deuces import Deck, Evaluator 



def run():
    deck = Deck()
    pile = deck.draw(3)
    hand = deck.draw(2)
    
    print(f'hand: {hand}')



# to do Q-Learning:
# - states
# - rewards
# 
# 
# 




if __name__ == "__main__":
    run()