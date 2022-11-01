#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *


# Goofspiel is played using cards from a standard deck of cards, and is typically a two-player game,[4] although more players are possible. Each suit is ranked A (low), 2, ..., 10, J, Q, K (high).
# 
# One suit is singled out as the "prizes"; each of the remaining suits becomes a hand for one player, with one suit discarded if there are only two players, or taken from additional decks if there are four or more. The prizes are shuffled and placed between the players with one card turned up.
# 
# Play proceeds in a series of rounds. The players make sealed bids for the top (face up) prize by selecting a card from their hand (keeping their choice secret from their opponent). Once these cards are selected, they are simultaneously revealed, and the player making the highest bid takes the competition card. Rules for ties in the bidding vary, possibilities including the competition card being discarded, or its value split between the tied players (possibly resulting in fractional scores).[1] Some play that the current prize "rolls over" to the next round, so that two or more cards are competed for at once with a single bid card.
# 
# The cards used for bidding are discarded, and play continues with a new upturned prize card.
# 
# After 13 rounds, there are no remaining cards and the game ends. Typically, players earn points equal to sum of the ranks of cards won (i.e. ace is worth one point, 2 is two points, etc., jack 11, queen 12, and king 13 points). Players may agree upon other scoring schemes.

# We need to translate the state to an observation, because of hidden info

# In[2]:


def initial_state():
    import random
    # state = prizes, hand1, hand2, played1,played2,current_turn_played
    # observation = top card of prizes, own hand, own played,other played
    
    # the current turn played will not show, because the moves are simultaneous
    
    hand1=CardList()
    hand2=CardList()
    prizes=CardList()
    for rank in range(1,13+1):
        hand1.append(Card(rank,'spades'))
        hand2.append(Card(rank,'clubs'))
        prizes.append(Card(rank,'hearts'))

    random.shuffle(prizes)
    
    played1=CardList()
    played2=CardList()
    current_turn_played=CardList()
    cards_won=CardList()
    
    state=prizes, hand1, hand2, played1,played2,cards_won,current_turn_played

    return state
    
def state_to_observation(state,player):
    prizes, hand1, hand2, played1,played2,cards_won,current_turn_played=state
    
    if not prizes:
        prizes=[None]
    
    if player==1:
        observation=prizes[0],hand1,played1,played2,cards_won
        
    else:
        observation=prizes[0],hand2,played2,played1,cards_won
        
    
    return observation


def score(played1,played2,cards_won,verbose=False):
    score1=0
    score2=0
    for c1,c2,cw in zip(played1,played2,cards_won):
        if c1.rank>c2.rank:
            score1+=cw.rank
            
            if verbose:
                print("\t",c1,'(*) ',c2," for ",cw)
            
        elif c1.rank<c2.rank:
            score2+=cw.rank
            if verbose:
                print("\t",c1,c2,'(*) '," for ",cw)
        else:  # tie - no score
            if verbose:
                print("\t",c1,' (=) ',c2," for ",cw)


    return score1,score2
    


def show_state(observation):
    print(observation)
    top_card,my_hand,my_played,other_played,cards_won=observation
    print("My hand:",[card for card in my_hand])
    print("Current Plays:")
    
    
    my_score,other_score=score(my_played,other_played,cards_won,verbose=True)
    print("My Score:",my_score)
    print("Other Score:",other_score)
    
    print("Top card:",top_card)

def valid_moves(observation,player):

    top_card,my_hand,my_played,other_played,cards_won=observation
    
    return my_hand


def update_state(state,player,move):
    prizes, hand1, hand2, played1,played2,cards_won,current_turn_played=state
    
    current_turn_played.append(move)
    
    if len(current_turn_played)==1:  # only first move
        new_state=prizes, hand1, hand2, played1,played2,cards_won,current_turn_played
        return new_state
    
    played1.append(current_turn_played[0])
    played2.append(current_turn_played[1])
    cards_won.append(prizes.pop(0))
    current_turn_played=CardList()
    
    new_state=prizes, hand1, hand2, played1,played2,cards_won,current_turn_played
    return new_state
    

def win_status(state,player):
    
    prizes, hand1, hand2, played1,played2,cards_won,current_turn_played=state
    
    if prizes: # end of the game only when the prizes are empty
        return None

    assert not current_turn_played
    assert len(played1)==len(played2)==len(cards_won)==13
    
    
    score1,score2=score(played1,played2,cards_won)

    if player==2:
        score1,score2=score2,score1
    
    if score1>score2:
        return 'win'
    elif score1<score2:
        return 'lose'
    else:
        return stalemate
    


# In[3]:


state=initial_state()


# In[4]:


show_state(state_to_observation(state,1))


# In[5]:


top_card,my_hand,my_played,other_played,cards_won=state_to_observation(state,1)


# In[6]:


[card.rank for card in my_hand]


# In[7]:


def random_move(state,player):

    moves=valid_moves(state,player)
    return random.choice(moves)

random_agent=Agent(random_move)


# In[8]:


def human_move(observation,player):
    top_card,my_hand,my_played,other_played,cards_won=observation
    ranks=[card.rank for card in valid_moves(observation,player)]
    print( "Player ", player)
    valid_move=False
    while not valid_move:
        move=int(input('What is the rank of the card to be played? '))

        if move in ranks:
            valid_move=True
        else:
            print( "Illegal move.")

            
    index=ranks.index(move)
    
    return my_hand[index]

human_agent=Agent(human_move)


# In[9]:


g=Game()
wins=g.run(random_agent,random_agent)


# In[ ]:




