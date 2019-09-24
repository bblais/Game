#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *
from Game.minimax import *

def initial_state():
    return Board(3,3)
    
def valid_moves(state,player):

    empty=[]
    for i in range(9):
        if state[i]==0:
            empty.append(i)

    return empty
    
    
def win_status(state,player):
    # in ttt, after a move, that player can either win or stalemate
    # they can't lose after their own move
    
    for i1,i2,i3 in [  [0,1,2],[2,5,8],[3,4,5],[6,7,8],
                    [0,3,6],[1,4,7], [0,4,8],[6,4,2]  ]:
        if state[i1]==player and state[i2]==player and state[i3]==player:
            return 'win'


    # stalemate
    tie=True
    for i in range(9):
        if state[i]==0:
            tie=False

    if tie:
        return 'stalemate'



def update_state(state,player,move):
    state[move]=player
    return state



def show_state(state):

    print(state)

def random_move(state,player):

    moves=valid_moves(state,player)
    return random.choice(moves)

def human_move(state,player):
    print( "Player ", player)
    valid_move=False
    while not valid_move:
        move=input('What is your move? ')
        move=int(move)

        if move in valid_moves(state,player):
            valid_move=True
        else:
            print( "Illegal move.")

    return move
    
human_agent=Agent(human_move)
random_agent=Agent(random_move)
   


# In[2]:


def heuristic(state,player):
    return 0

def minimax_move(state,player):

    values,moves=minimax_values(state,player,maxdepth=4)
    values,moves=minimax_values(state,player)
    
    
    return top_choice(moves,values)
    
    
minimax_agent=Agent(minimax_move)


# In[3]:


g=Game()
wins=g.run(minimax_agent,human_agent)

g.report()


# In[4]:


state=initial_state()


# In[5]:


minimax_values(state,1)


# In[ ]:




