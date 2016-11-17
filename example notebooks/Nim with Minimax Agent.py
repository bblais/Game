
# coding: utf-8

# In[10]:

from Game import *
from Game.minimax import *


# ## Minimum necessary functions

# In[11]:

def initial_state():
    return 21


# In[12]:

def valid_moves(state,player):

    if state==1:
        return [1]
    elif state==2:
        return [1,2]
    else:
        return [1,2,3]
 


# In[13]:

def show_state(state):
    print("There are ",state," sticks left.")


# In[14]:

def update_state(state,player,move):
    new_state=state-move
    return new_state


# In[15]:

def win_status(state,player):
    if state==1:
        return 'win'
    elif state==0:
        return 'lose'    
    else:
        return None


# ## Agents

# In[16]:

# agents

def random_move(state,player):
    moves=valid_moves(state,player)
    return random.choice(moves)

def human_move(state,player):
    move=eval(input('Take 1, 2 or 3 sticks '))
    return move


def minimax_move(state,player):

    values,moves=minimax_values(state,player)
    return top_choice(moves,values)
    
    
minimax_agent=Agent(minimax_move)
human_agent=Agent(human_move)
random_agent=Agent(random_move)


# ## Run against a person

# In[17]:


g=Game(number_of_games=1)
g.run(human_agent,minimax_agent)
g.report()


# ## Run many times

# In[18]:


g=Game(number_of_games=100)
g.display=False
g.run(minimax_agent,random_agent)
g.report()


# In[ ]:



