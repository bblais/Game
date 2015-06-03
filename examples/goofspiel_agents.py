from Game import Agent
import random

def lowhigh(hand,shown,info=None):
    return hand[0]
    
def highlow(hand,shown,info=None):
    return hand[-1]
    
highlow_agent=Agent(highlow)
highlow_agent.name='HiLo'

lowhigh_agent=Agent(lowhigh)
lowhigh_agent.name='LoHi'

def human_move(hand,shown,info=None):

    print "Your hand is:",hand
    while True:
        rank=input('What is your bet (give the rank)? ')
        
        card=[x for x in hand if x.rank==rank]
        if card:
            return card[0]
        else:
            print rank, "Not in hand."
    
    return card
    
    
def random_move(hand,shown,info=None):
    return random.choice(hand)
    

human_agent=Agent(human_move)
human_agent.name='Human'

random_agent=Agent(random_move)
random_agent.name='Randy'
