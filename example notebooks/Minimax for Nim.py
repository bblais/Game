#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *
from Game.minimax import *


def initial_state():
    return 21

def valid_moves(state,player):
    if state==1:
        return [1]
    elif state==2:
        return [1,2]
    else:
        return [1,2,3]
        
def show_state(state):
    print ("There are ",state," sticks left.")

def update_state(state,player,move):
    new_state=state-move
    return new_state

def win_status(state,player):

    if state==1:
        return 'win'
    
    elif state==0:
        return 'lose'
    
    else:
        return None

def random_move(state,player):
    move=random.choice(valid_moves(state,player))
    return move


def human_move(state,player):

    move=input('Take 1, 2 or 3 sticks ')
    return move


def minimax_move(state,player):

    values,moves=minimax_values(state,player)
    return top_choice(moves,values)
    
    
minimax_agent=Agent(minimax_move)
random_agent=Agent(random_move)
human_agent=Agent(human_move)


# ## Running typical minimax

# In[2]:


g=Game()
wins=g.run(random_agent,minimax_agent)

g.report()


# In[3]:


minimax_values(6,1)


# when in a losing position, all the values are the same

# In[4]:


minimax_values(5,1)


# ## Dealing with the long or infinite game problem

# In[5]:


def initial_state():
    return 27


# In[6]:


values,moves=minimax_values(27,1)  # was about 2 seconds


# In[9]:


values,moves=minimax_values(31,1)


# In[10]:


values,moves


# when the game is long (say the initial state is large), minimax takes a long time

# In[22]:


g=Game()
wins=g.run(random_agent,minimax_agent)
g.report()


# what we can do is to set a maximum minimax depth.  When reaching this depth, and it isn't the game, the simulator gets a value from the function called heuristic.  This is just a rule of thumb, and shouldn't return a -1 or 1 (which would be certain of the penalty).  In this case I realize that odd numbers tend to be worse than even numbers, so return a middle value.  it won't play a perfect game, unless that game is shorter than the maximum depth.

# In[23]:


def minimax_move(state,player):

    values,moves=minimax_values(state,player,maxdepth=5)
    return top_choice(moves,values)
    
def heuristic(state,player):
    # handing the oppponent the state, is this good for you (positive) or bad for you (negative)
    if state%2 == 0: # giving the opponent an even number tends to be bad
        return -0.5
    else:
        return 0.5 # giving the opponent an odd number tends to be good
    
    # if you're just interested penalizing long games, just return zero.
    
minimax_agent=Agent(minimax_move)


# In[24]:


minimax_values(15,1,maxdepth=5)


# In[25]:


minimax_values(15,1)


# In[27]:


print (minimax_values(27,1,maxdepth=5))
print (minimax_values(27,1))


# In[28]:


g=Game()
wins=g.run(random_agent,minimax_agent)
g.report()


# ## Dealing with fatalistic agent
# 
# When faced with an all-losing situation, one should really value long losing games as better than short losing games, to give the opponent a chance to make mistakes.

# In[29]:


def minimax_move(state,player):
    values,moves=minimax_values(state,player,adjust_values_by_depth=True)
    return top_choice(moves,values)
minimax_agent=Agent(minimax_move)


# In[31]:


print (minimax_values(14,1,adjust_values_by_depth=True))


# this doesn't work quite as well in nim, because every game from a given state has the same length against a perfect player, so it has the same depth.  should work for tic tac toe.
