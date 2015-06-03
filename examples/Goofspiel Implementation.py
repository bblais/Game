# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division
from Game import *
from copy import deepcopy

# <codecell>

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

# <codecell>

deck,hands=initial_state(4)
deepcopy(hands)

# <codecell>

state=initial_state()
print state

# <codecell>

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
 

# <codecell>

def play(agents,number_of_cards=4,
        number_of_games=1,display=True):
    
    all_scores=[]

    for game in range(number_of_games):    
    
    
        for agent in agents:
            agent.states=[]
            agent.actions=[]
            agent.last_action=None
            agent.last_state=None
            agent.last_player=None
    
    
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
            use_full_state=False
            
            for hand,agent in zip(hands,agents):
                
                if use_full_state:
                    # the full state here should be all of the hands, the shown, and the deck!
                    # make the current hand the first in the hands state

                    state_hands=[hand]
                    for hand2 in hands:
                        if hand2 not in state_hands:
                            state_hands.append(hand2)

                    state=[state_hands, shown, deck]
                    
                else:
                    # the partial state is just your hand, and that shown
                    state=[hand, shown]
                    
                card=agent.move(state,agent)
                move=card
                
                agent.states.append(deepcopy(state))
                agent.actions.append(deepcopy(move))
                agent.last_action=deepcopy(move)
                agent.last_state=deepcopy(state)

                hand.remove(card)
                moves.append(card)
                
                
                
                
            if display:
                for agent,move in zip(agents,moves):
                    print "%s chooses card %s" % (agent.name,move)
            
            winners=get_winners(moves)
            score_adjust=shown.rank/len(winners)  # score is divided among winners

            for i,agent in enumerate(agents):
                if i in winners:
                    reward=score_adjust
                else:
                    reward=0
                    
                try:
                    agent.post(reward,agent)
                except (AttributeError,KeyError):
                    pass
                    
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

# <markdowncell>

# ## Agents

# <codecell>

def lowhigh(state,info=None):
    if len(state)==3:  # full state
        all_hands,shown,deck=state
        hand=all_hands[0]
    else:
        hand,shown=state
        
    return hand[0]
    
def highlow(hand,shown,info=None):
    if len(state)==3:  # full state
        all_hands,shown,deck=state
        hand=all_hands[0]
    else:
        hand,shown=state
    return hand[-1]
    
highlow_agent=Agent(highlow)
highlow_agent.name='HiLo'

lowhigh_agent=Agent(lowhigh)
lowhigh_agent.name='LoHi'

# <codecell>

def human_move(state,info=None):
    if len(state)==3:  # full state
        all_hands,shown,deck=state
        hand=all_hands[0]
        print "The other hands are:",all_hands[1:]
        print "Remaining in deck is:",deck
    else:
        hand,shown=state
        
    print "Your hand is:",hand
    print "Shown is:",shown
    while True:
        rank=input('What is your bet (give the rank)? ')
        
        card=[x for x in hand if x.rank==rank]
        if card:
            return card[0]
        else:
            print rank, "Not in hand."
    
    return card
    
    
human_agent=Agent(human_move)
human_agent.name='Human'

# <codecell>

def random_move(state,info=None):
    if len(state)==3:  # full state
        all_hands,shown,deck=state
        hand=all_hands[0]
    else:
        hand,shown=state
    return random.choice(hand)
random_agent=Agent(random_move)
random_agent.name='Flip'

# <codecell>

import sys
def Q_move(state,info):
    if len(state)==3:  # full state
        all_hands,shown,deck=state
        hand=all_hands[0]
    else:
        hand,shown=state
    
    Q=info.Q
    last_action=info.last_action
    last_state=info.last_state
    
    alpha=info.alpha  # learning rate
    gamma=info.gamma  # memory 
    epsilon=info.epsilon  # probability of doing random move

    if not state in Q:
        Q[state]=Table()
        for action in hand:
            Q[state][action]=0.0
            
    if random.random()<epsilon:  # random move
        action=random_choice(Q[state])
    else:
        action=top_choice(Q[state])
        
        
    if not last_action is None:  # anything but the first move
        r=0.0
        Q[last_state][last_action]+=alpha*(r + 
            gamma*max([Q[state][a] for a in Q[state]]) -
            Q[last_state][last_action] )
        
    return action

def Q_post(reward,info):
    Q=info.Q
    last_action=info.last_action
    last_state=info.last_state
    
    alpha=info.alpha  # learning rate
    gamma=info.gamma  # memory 
    epsilon=info.epsilon  # probability of doing random move

    r=reward
        
    if not last_action is None:  # anything but the first move
        Q[last_state][last_action]+=alpha*(r -
            Q[last_state][last_action] )
        

# <codecell>

Q_agent=Agent(Q_move)
Q_agent.post=Q_post
Q_agent.name="Queuey"

Q_agent.Q=Remember(filename='Q_data.dat')
Q_agent.alpha=0.3  # learning rate
Q_agent.gamma=0.9  # memory
Q_agent.epsilon=0.1  # chance of making a random move

# <markdowncell>

# ## Run the Game

# <codecell>

agents=[random_agent,Q_agent]

scores=play(agents,
            number_of_cards=4,
            number_of_games=1000,
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

Remember(Q_agent.Q,filename='Q_data.dat')


# <codecell>


