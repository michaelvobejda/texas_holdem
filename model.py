from deuces import Card


def run():
    deck = d.Deck()
    pile = deck.draw(3)
    hand = deck.draw(2)
    
    print(f'hand: {hand}')



# to do Q-Learning:
# - states
# - rewards



if __name__ == "__main__":
    run() 