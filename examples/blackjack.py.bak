from __future__ import division
from Game import *

def value(hand):
    has_ace=False
    val=0
    for card in hand:
        if card.rank==1:
            has_ace=True
            
        if card.rank>10:
            val+=10
        else:
            val+=card.rank
        
    if has_ace and val+10<21:
        val+=10
        
    return val



def play(agents,number_of_decks=1,
        number_of_games=1,display=True):

    all_scores=[]

    for agent in agents:
        agent.score=0

    for game in range(number_of_games):    
    
        deck=makedeck(number_of_decks,shuffle=True)
        hands=[]
        # deal two for every agent
        for agent in agents:
            agent.hand=deal(deck,2)
            hands.append(agent.hand)
            
        for agent in agents:
            # shown is all of the cards for all agents, 
            # except the first card
            shown={}
            for agent2 in agents:
                shown[agent2.name]=agent2.hand[1:]

            hand=agent.hand
            
            if display:
                print agent.name,"'s move"
                print "\tShown is ",shown
                print "\tYour hand is:",hand
                
            while True:  # keep going until stay or bust
                move=agent.move(hand,shown,agent)
                if display:
                    print "\t Move: ",move
                if move=='s':
                    break
                agent.hand.extend(deal(deck))

                if display:
                    print agent.name
                    print "\tShown is ",shown
                    print "\tYour hand is:",hand

                if value(agent.hand)>21:
                    if display:
                        print "\tBust!"
                    break

        if display:
            print "Results"
            for agent in agents:
                print agent.name
                print "\t",agent.hand
                print "\t",value(agent.hand)
                if value(agent.hand)>21:
                    print "\t\tBust!"
                    
                
        winners=[]
        max_so_far=-1
        for agent in agents:
            score=value(agent.hand)
            if score>21:  # busting doesn't win
                continue
            if score>max_so_far:
                winners=[agent]
                max_so_far=score
            elif score==max_so_far:
                winners.append(agent)
                max_so_far=score
            else:
                pass
                
        # dealer wins in a tie
        if dealer_agent in winners:
            winners=[dealer_agent]

        if display:
            print "Winners:"
            for agent in winners:
                print "\t",agent.name
                
        for agent in winners:
            agent.score+=1

        if display:
            print "================="
          
    return [agent.score for agent in agents]
    
def dealer_move(hand,shown,info=None):

    val=value(hand)
    if val<=16:
        return 'h'
    else:
        return 's'


def human_move(hand,shown,info=None):
    move=raw_input('Hit or stay? ')    
    move=move.lower()[0]
    return move    
    
def random_move(hand,shown,info=None):
    return random.choice(['h','s'])
    

human_agent=Agent(human_move)
human_agent.name='Human'

dealer_agent=Agent(dealer_move)
dealer_agent.name='Dealer'

random_agent=Agent(random_move)
random_agent.name='Bob'
    

   
agents=[human_agent,random_agent,dealer_agent]

scores=play(agents,
            number_of_games=2,
            display=True)
            
