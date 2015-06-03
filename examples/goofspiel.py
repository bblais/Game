from __future__ import division
from Game import *
from goofspiel_agents import *

def copy_move_pre(info=None):
    info.old_game=Remember(filename='cooly_memory.dat')
    info.new_game=Table()

def copy_move(hand,shown,info=None):
    pass
    
def copy_move_post(status,player,info=None):
    Remember(info.new_game,filename='cooly_memory.dat')


def initial_state(N=13):  # this is the full state
    deck=[]
    for rank in range(1,N+1):
        for suit in ['h']:
            c=Card(rank,suit)
            deck.append(c)

    random.shuffle(deck)

    hands=[]
    hand=[]
    for rank in range(1,N+1):
        for suit in ['s']:
            c=Card(rank,suit)
            hand.append(c)
    hands.append(hand)
    
    hand=[]
    for rank in range(1,N+1):
        for suit in ['c']:
            c=Card(rank,suit)
            hand.append(c)
    hands.append(hand)
    
    return deck,hands

    
def get_winners(moves): 
    winners=[]
    vals=[card.rank for card in moves]
    
    max_so_far=-1    
    for player,val in enumerate(vals):
    
        if val>max_so_far:
            winners=[player]
            max_so_far=val
        elif val==max_so_far:
            winners.append(player)
            
    return winners
  
def play(agents,number_of_cards=4,
        number_of_games=1,display=True):
    
    all_scores=[]

    for game in range(number_of_games):    
    
        deck,hands=initial_state(number_of_cards)
        scores=[0]*len(agents)
        
        
        
        for round in range(len(deck)):
            
            if display:
                print 'Current Scores: '
                for agent,score in zip(agents,scores):
                    print '\t',agent.name,':',score
            
            shown=deal(deck)[0]
            
            if display:
                print "Card shown is: ",shown
            
            moves=[]
            for hand,agent in zip(hands,agents):
                card=agent.move(hand,shown,agent)
                if display:
                    print "%s chooses card %s" % (agent.name,str(card))
                hand.remove(card)
                moves.append(card)
            
            winners=get_winners(moves)
            score_adjust=shown.rank/len(winners)  # score is divided among winners
            
            for winner in winners:
                if display:
                    print agents[winner].name,"wins",score_adjust
                scores[winner]+=score_adjust

        if display:        
            print
            print 'Final Scores: '
            for agent,score in zip(agents,scores):
                print '\t',agent.name,':',score
            print "\n===\n"
            
        all_scores.append(scores)
    
    return all_scores


agents=[highlow_agent,random_agent]

scores=play(agents,
            number_of_cards=4,
            number_of_games=100,
            display=False)
            
wins=[0,0,0]
for score in scores:
    if score[0]>score[1]:
        wins[0]+=1
    elif score[1]>score[0]:
        wins[1]+=1
    else:
        wins[2]+=1
        
print agents[0].name,' won ',wins[0],'times.'
print agents[1].name,' won ',wins[1],'times.'
print wins[2],'ties.'
    
