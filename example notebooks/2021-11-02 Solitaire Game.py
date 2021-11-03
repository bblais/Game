#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *


# There are k cards in the deck. There is a card with the number 1 on it, a card with the
# number 2 on it, and so forth, up to the card with the number k on it. These cards are
# shuffled face down, and then you flip them over one at a time.
# Your goal is to get as many cards as possible onto a victory pile. The victory pile starts out
# empty. The cards must be placed onto the victory pile in ascending numerical order. The
# first card placed on the victory pile must be the card with the number 1 on it, followed
# by the card with the number 2 on it, etc.
# You are allowed two discard piles. Any time you flip a card from the deck and you can’t
# (or choose not to) put it immediately onto the victory pile, you place it face up onto one
# of the discard piles.
# At any point in the game, you are allowed to take the top card off of either of the discard
# piles, and move it onto the victory pile, if it is the appropriately numbered card to do so.
# You are not allowed to move the top card from one discard pile to the other
# discard pile.
# The game is over when you have flipped through all k cards in the deck, and you have
# moved as many cards as you can onto the victory pile.
# Vegas is charging you $5 to play the game, and paying out $1 for every card you get
# onto the victory pile. For this assignment, you will use data structures discussed in class
# 1
# and come up with a strategy for how to best use your discard piles to optimize your
# performance.
# You will write a program to simulate the play of the game and determine whether you’d
# get rich or go bankrupt in the long run.

# In[2]:


def initial_state(k=10):
    
    deck=[]
    for rank in range(1,k+1):
        deck.append(Card(rank=rank,suit='s'))
        
    random.shuffle(deck)
    dealt=deal(deck,1)[0]
    return [deck,dealt,[],[],[]]  # deck, dealt card,victory pile, dicard pile,discard pile2


# In[3]:


initial_state()


# In[4]:


def show_state(state):
    print(state)


# In[5]:


def state_to_observation(state,player):
    return [state[1],state[2][-1:],state[3][-1:],state[4][-1:]]


# In[6]:


state_to_observation(initial_state(),1)


# In[7]:


def valid_moves(state,player):
    dealt,V,D1,D2=state
    
    moves=[]
    
    if not V and dealt:
        moves.append("V")
    elif dealt and dealt.rank>V[-1].rank:
        moves.append("V")

    if dealt:
        moves.append("D1")
        moves.append("D2")
    
    if D1 and not V:
        moves.append("D1toV")
    elif D1 and D1[-1].rank>V[-1].rank:
        moves.append("D1toV")
        
    if D2 and not V:
        moves.append("D2toV")
    elif D2 and D2[-1].rank>V[-1].rank:
        moves.append("D2toV")
    
    return moves  # victory, discard1, discard2


# In[ ]:





# In[8]:


def update_state(state,player,move):  # this is the full state
    
    deck,dealt,V,D1,D2=state
    
    if move=="V":
        V.append(dealt)
        if deck:
            dealt=deal(deck,1)[0]
        else:
            dealt=None
            
    elif move=="D1":
        
        D1.append(dealt)
        if deck:
            dealt=deal(deck,1)[0]
        else:
            dealt=None
        
    elif move=="D2":
        
        D2.append(dealt)
        if deck:
            dealt=deal(deck,1)[0]
        else:
            dealt=None
            
    elif move=="D1toV":
        V.append(D1.pop())
    elif move=="D2toV":
        V.append(D2.pop())
    
    else:
        raise ValueError("You can't get there from here.")
        
        
    new_state=deck,dealt,V,D1,D2
    return new_state
        


# In[9]:


def win_status(state,player):
    
    deck,dealt,V,D1,D2=state
    
    try:
        if deck or dealt:
            return

        if not V:
            return

        if D1 and D1[-1].rank>V[-1].rank:
            return

        if D2 and D2[-1].rank>V[-1].rank:
            return

        return "stalemate"
    except AttributeError:
        print(state)
        raise


# In[10]:


def Q_move(state,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ
    
    if state not in Q:
        actions=valid_moves(state,player)
        Q[state]=Table()
        for action in actions:
            Q[state][action]=0  # initial value of table

    if not learning:
        ϵ=0
    
    if random.random()<ϵ:  # take a random move occasionally to explore the environment
        move=random_move(state,player)
    else:
        move=top_choice(Q[state])
    
    if not last_action is None:  # not the first move
        reward=0
        
        # learn
        if learning:
            Q[last_state][last_action]+=α*(reward +
                        γ*max([Q[state][a] for a in Q[state]]) - Q[last_state][last_action])
    
    return move


# In[10]:


    
def Q_after(status,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ


    
    dealt,V,D1,D2=last_state
    
    reward=len(V)-5
    info.rewards.append(reward)
        
    if learning:
        Q[last_state][last_action]+=α*(reward - Q[last_state][last_action])
        


# In[11]:


Q1_agent=Agent(Q_move)
Q1_agent.post=Q_after
Q1_agent.Q=Table()  # makes an empty table
Q1_agent.learning=True
Q1_agent.rewards=[]

Q1_agent.α=0.3  # learning rate
Q1_agent.ϵ=0.5  # how often to take a random move
Q1_agent.γ=0.9  # memory constant -- how quickly does the table update back in time (earlier in the game)

Q2_agent=Agent(Q_move)
Q2_agent.post=Q_after
Q2_agent.Q=Q1_agent.Q  # makes an empty table
Q2_agent.learning=True
Q2_agent.rewards=[]

Q2_agent.α=Q1_agent.α  # learning rate
Q2_agent.ϵ=Q1_agent.ϵ  # how often to take a random move
Q2_agent.γ=Q1_agent.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)


# In[11]:


def random_after(status,player,info):
    last_state=info.last_state
    last_action=info.last_action
    dealt,V,D1,D2=last_state
    reward=len(V)-5
    info.rewards.append(reward)

    
def random_move(state,player):
    
    move=random.choice(valid_moves(state,player))
    return move


random_agent=Agent(random_move)
random_agent.post=random_after
random_agent.rewards=[]


# In[12]:


agent1=Q1_agent
agent2=Q2_agent


# agent1=random_agent
# agent2=random_agent


# In[13]:


from tqdm import tqdm
from numpy import mean


# In[14]:


N_train=5000
N_test=100
number_of_epochs=200

agent1_test=None
agent2_test=None


iteration_count=0
number_of_iterations=[]
average_reward=[]


for i in range(number_of_epochs):

    agent1.learning=True
    agent2.learning=True

    g=Game(number_of_games=N_train)
    g.display=False
    result=g.run(agent1,agent2)

    number_of_iterations.append(iteration_count)

    if agent1_test is None:
        agent1_test=agent1
    if agent2_test is None:
        agent2_test=agent2

    # turn learning off to test
    agent1_test.learning=False
    agent2_test.learning=False

    agent1_test.rewards=[]
    agent2_test.rewards=[]
    
    
    g=Game(number_of_games=N_test)
    g.display=False
    result=g.run(agent1_test,agent2_test)
    iteration_count+=N_train
    
    average_reward.append(mean(agent1.rewards))
    print(mean(agent1.rewards),mean(agent2.rewards))


# In[15]:


Q1_agent.Q


# In[ ]:




