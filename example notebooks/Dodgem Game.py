#!/usr/bin/env python
# coding: utf-8

# Dodgem Rules:
# Move forward, left, or right to get across the board and around your opponent. When you reach the opposite side of the board move to position -1 to remove the piece from the board. First to remove all their pieces wins.

# In[1]:


from Game import*


# In[2]:


from Game import *
from Game.mcts import *


# In[3]:


def initial_state(): #initial state is a nxn board with n-1 cars for each team on the left and bottom leaving the corner open
    state=Board(3,3)
    state[0]=1
    state[3]=1
    state[7]=2
    state[8]=2
    return state


# In[4]:


state=initial_state()
state


# In[5]:


def show_state(state):
    print(state[0],state[1],state[2])
    print(state[3],state[4],state[5])
    print(state[6],state[7],state[8])


# In[6]:


show_state(state)


# In[7]:


def valid_moves(state, player):
    #note to self: move=[start,end]
    moves=[]
    #player 1 valid moves
    if player==1:
        if state[0]==1 and state [1]==0:
            move=[0,1]
            moves.append(move)
        if state[3]==1 and state [4]==0:
            move=[3,4]
            moves.append(move)
        if state[1]==1 and state [2]==0:
            move=[1,2]
            moves.append(move)
        if state[4]==1 and state [5]==0:
            move=[4,5]
            moves.append(move)
        if state[6]==1 and state [7]==0:
            move=[6,7]
            moves.append(move)
        if state[7]==1 and state [8]==0:
            move=[7,8]
            moves.append(move)
        if state[0]==1 and state [3]==0:
            move=[0,3]
            moves.append(move)
        if state[3]==1 and state [0]==0:
            move=[3,0]
            moves.append(move)
        if state[3]==1 and state [6]==0:
            move=[3,6]
            moves.append(move)
        if state[6]==1 and state [3]==0:
            move=[6,3]
            moves.append(move)
        if state[1]==1 and state [4]==0:
            move=[1,4]
            moves.append(move)
        if state[4]==1 and state [1]==0:
            move=[4,1]
            moves.append(move)
        if state[4]==1 and state [7]==0:
            move=[4,7]
            moves.append(move)
        if state[7]==1 and state [4]==0:
            move=[7,4]
            moves.append(move)
        if state[2]==1 and state [5]==0:
            move=[2,5]
            moves.append(move)
        if state[5]==1 and state [2]==0:
            move=[5,2]
            moves.append(move)
        if state[5]==1 and state [8]==0:
            move=[5,8]
            moves.append(move)
        if state[8]==1 and state [5]==0:
            move=[8,5]
            moves.append(move)
          #removing piece from board  
        if state[2]==1:
            move=[2,-1]
            moves.append(move)
        if state[5]==1:
            move=[5,-1]
            moves.append(move)
        if state[8]==1:
            move=[8,-1]
            moves.append(move)

    #player 2 valid moves 1 0 0
    #                     1 0 0
    #                     0 2 2
    if player==2:
        if state[8]==2 and state [5]==0:
            move=[8,5]
            moves.append(move)
        if state[5]==2 and state [2]==0:
            move=[5,2]
            moves.append(move)
        if state[7]==2 and state [4]==0:
            move=[7,4]
            moves.append(move)
        if state[4]==2 and state [1]==0:
            move=[4,1]
            moves.append(move)
        if state[6]==2 and state [3]==0:
            move=[6,3]
            moves.append(move)
        if state[3]==2 and state [0]==0:
            move=[3,0]
            moves.append(move)
        if state[8]==2 and state [7]==0:
            move=[8,7]
            moves.append(move)
        if state[7]==2 and state [8]==0:
            move=[7,8]
            moves.append(move)
        if state[7]==2 and state [6]==0:
            move=[7,6]
            moves.append(move)
        if state[6]==2 and state [7]==0:
            move=[6,7]
            moves.append(move)
        if state[5]==2 and state [4]==0:
            move=[5,4]
            moves.append(move)
        if state[4]==2 and state [5]==0:
            move=[4,5]
            moves.append(move)
        if state[4]==2 and state [3]==0:
            move=[4,3]
            moves.append(move)
        if state[3]==2 and state [4]==0:
            move=[3,4]
            moves.append(move)
        if state[2]==2 and state [1]==0:
            move=[2,1]
            moves.append(move)
        if state[1]==2 and state [2]==0:
            move=[1,2]
            moves.append(move)
        if state[1]==2 and state [0]==0:
            move=[1,0]
            moves.append(move)
        if state[0]==2 and state [1]==0:
            move=[0,1]
            moves.append(move)
        # player 2 removing piece from board    
        if state[0]==2:
            move=[0,-1]
            moves.append(move)
        if state[1]==2:
            move=[1,-1]
            moves.append(move)
        if state[2]==2:
            move=[2,-1]
            moves.append(move)
        
    return moves


# In[8]:


def human_move(state, move, player):
    print('Player',player)
    valid_moves=false
    while not valid_moves:
        move=input('What is your move? ')

        if move in valid_moves(state, move, player):
            valid_move=True
        else:
            print("Illegal move.")

    return move


# In[9]:


def update_state(state,player,move):
    start,end=move
    
    if end>-1:
        state[start]=0
        state[end]=player
    else:
        state[start]=0
        
    return state


# In[10]:


def win_status(state, player):
    if player==1 and not 1 in state:
        return 'win'
    if player==2 and not 2 in state:
        return 'win'
    
    if player==1:
        other_player=2
    else:
        other_player=1
        
    if not valid_moves(state, other_player):
        return 'lose'


# In[11]:


def  get_human_move(state,player):
    print('Player',player)
    move=[int(input('What is your start position?')),int(input('What is your end position?'))]
    return move


# In[12]:


def  random_move(state,player):
    moves=valid_moves(state,player)
    return random.choice(moves)


# In[13]:


show_state(state)


# In[14]:


human_agent=Agent(get_human_move)
random_agent=Agent(random_move)


# In[15]:


def mcts_move(state,player,info):
    T=info.T
    values,moves=mcts_values(state,player,T,info.seconds)
    
    if isinstance(values,int):
        print("values",values)
        print("moves",moves)
    
        print("state",state)
        print("player",player)
        print(T)
    return top_choice(moves,values)

mcts_agent=Agent(mcts_move)
mcts_agent.T=Table()
SaveTable(mcts_agent.T,filename='mcts_dodgem_data.json')
mcts_agent.seconds=.2


# In[25]:


mcts_agent.T=LoadTable(filename='mcts_dodgem_data.json')


# In[26]:


g=Game()
g.display=False
games=100
wins=g.run(random_agent,mcts_agent)
g.report()
SaveTable(mcts_agent.T,filename='mcts_dodgem_data.json')


# In[27]:


mcts_agent.T


# In[ ]:


state=Board(3,3)
state.board=[0,  0 , 1 , 0 , 1 , 2 , 0 , 0 , 2 ]


# In[ ]:


state


# In[ ]:


mcts_agent.seconds=-1
mcts_move(state,2,mcts_agent)


# In[ ]:


current_state=state
player=2
T=mcts_agent.T


# In[ ]:


moves=valid_moves(current_state,player)
moves


# In[ ]:


available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]    


# In[ ]:


percent_wins,move=max(
    (T[(S,player)].get('wins',0)/T[(S,player)].get('plays',1),
     move) for S,move in zip(available_states,moves)
)
  


# In[ ]:


percent_wins,move


# In[ ]:




