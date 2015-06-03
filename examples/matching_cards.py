from __future__ import division
from Game import *

# not sure if this is a real game, but here goes
# each player is dealt 10 cards
# another card from the deck is is shown face-up, and is trump
# and the play proceeds with choices
# from each player that must match the suit dealt up (if you can)
# or can be trump
# highest trump card wins, then highest matching card, 
# then highest card player
# score is updated by number of trump cards taken
# ace is low

def valid_cards(hand,shown,trump_card):
    # must match suit, if you can, or play trump
    valid=[]
    for card in hand:
        if card.suit==shown['_up_'].suit:
            valid.append(card)

    if not valid:  # can return anything
        return hand
    else: # add the trump cards too
        for card in hand:
            if card in valid:
                continue  # don't count cards twice
                
            if card.suit==trump_card.suit:
                valid.append(card)

        return valid
        
def choose_card(hand):
    for i,card in enumerate(hand):
        print "[%d] %s" % (i+1,str(card))
        
    valid=False
    while not valid:
        response=raw_input('Which card? ')
        try:
            cardnum=int(response)-1
            if cardnum<0 or cardnum>=len(hand):
                print "Illegal move"
            else:
                valid=True
        except ValueError:
            print "Illegal move (please enter a card number)"
        
    return hand[cardnum]
       
def human_move(hand,shown,info=None):
    move=choose_card(hand)
    return move    
    
def random_move(hand,shown,info):
    valid=valid_cards(hand,shown,info.trump_card)
    return random.choice(valid)
       
       
       
def play(agents,number_of_decks=1,
        number_of_games=1,display=True):

    all_scores=[]

    for agent in agents:
        agent.score=0

    for game in range(number_of_games):    
    
        deck=makedeck(number_of_decks,shuffle=True)
        hands=[]
        collection={}

        # deal 10 for every agent
        for agent in agents:
            agent.hand=deal(deck,10)
            hands.append(agent.hand)
            collection[agent.name]=[]

        collection['_up_']=[]
        
        trump_card=None
        for trick in range(10):
            up_card=deal(deck)[0]
            
            shown={}
            shown['_up_']=up_card
            if trump_card is None:
                trump_card=up_card  # first up card is trump
            
            for agent in agents:
                # shown is all of the choices of the agents
                # and the up card
                agent.trump_card=trump_card
                
                hand=agent.hand
                
                if display:
                    print agent.name,"'s move"
                    print "\tShown is ",shown
                    print "\tYour hand is:",hand
                    
                valid=False
                while not valid:
                    card_choice=agent.move(hand,shown,agent)
                    if card_choice not in valid_cards(hand,shown,trump_card):
                        print "Illegal move",card_choice
                    else:
                        valid=True
                                        
                if display:
                    print "\t Move: ",card_choice
                    
                agent.hand.remove(card_choice)
                shown[agent.name]=card_choice

            # after going through all the agents in a trick
            # figure out who collects

            max_so_far=Card(0,'s')  #minimum card
            max_name=None
            
            # check for max trump
            for name in shown:
                card=shown[name]
                if card.suit==trump_card.suit:
                    if card.rank>max_so_far.rank:
                        max_so_far=card
                        max_name=name
                        
            if max_name is None:  # no trumps found, highest matching up
                for name in shown:
                    card=shown[name]
                    if card.suit==up_card.suit:
                        if card.rank>max_so_far.rank:
                            max_so_far=card
                            max_name=name
            
            cards=[shown[name] for name in shown]
            if display:
                if max_name=='_up_':
                    print "no winner"
                else:
                    print max_name,"wins trick",cards
                    
            collection[max_name].extend(cards)
            print "---------------"
                

        for agent in agents:
            count=0
            for card in collection[agent.name]:
                if card.suit==trump_card.suit:
                    count+=1
            agent.trump_count=count
        
        if display:
            print "Results"
            for agent in agents:
                print agent.name
                print "\t",collection[agent.name]
                print "\tNumber of trump:",agent.trump_count
                
        for agent in agents:
            agent.score+=agent.trump_count

        if display:
            print "Current scores:"
            for agent in agents:
                print "\t%s: %d" % (agent.name,agent.score)

        if display:
            print "================="
          
    return [agent.score for agent in agents]

agents=[]

human_agent=Agent(human_move)
human_agent.name='Human'

random_agent1=Agent(random_move)
random_agent1.name='Bob'

random_agent2=Agent(random_move)
random_agent2.name='Bill'

random_agent3=Agent(random_move)
random_agent3.name='Brian'


agents=[human_agent,random_agent1,random_agent2,random_agent3]

scores=play(agents,
            number_of_games=2,
            display=True)




