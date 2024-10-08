#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from pylab import *


# In[2]:


from Game import*


# Four functions to do:
# 
# 1. initial_state() return state for the start of the game
# 2. valid_moves(state,player) return a list of valid moves
# 3. update_state(state, player, move) return the new state
# 4. win_status (new_state, player) retunrs one of "win", "lose", "stalemate" or "none"
# 
# - What is state for this game: board, 4x5, 20#s
# - what is a move for this game: sigle 

# #Minimax can be found after the monkey agent function

# In[3]:


def initial_state():
    return Board(4,5)


# In[4]:


def valid_moves(state,player):
    moves=[]
    
    for i in range(5):
        if state[i]==0:
            moves.append(i)
            
    return moves
        


# In[5]:


# Here, since there are 5 columns to "drop" a piece in, i in range is 5


# In[6]:


def update_state(state,player,move):
    new_state=state
    col=move
    for row in range(3,-1,-1):
        if state[row,col]==0:
            break
    state[row,col]=player
    
    return new_state
# Here, we want to loop rows from the bottom, and when zero is hit it breaks out. This ensures proper stacking of moves


# In[7]:


def win_status(state,player):
# 0  1  2  3   4 
# 5  6  7  8   9 
# 10 11 12 13 14 
# 15 16 17 18 19
    
        if player==1:
            other_player=2
        else:
            other_player=1
# Horizontal right wins
        if state[0]==player and state[1]==player and state[2]==player:
            return "win"
        if state[1]==player and state[2]==player and state[3]==player:
            return "win"
        if state[2]==player and state[3]==player and state[4]==player:
            return "win"
        if state[5]==player and state[6]==player and state[7]==player:
            return "win"
        if state[6]==player and state[7]==player and state[8]==player:
            return "win"
        if state[7]==player and state[8]==player and state[9]==player:
            return "win"
        if state[10]==player and state[11]==player and state[12]==player:
            return "win"
        if state[11]==player and state[12]==player and state[13]==player:
            return "win"
        if state[12]==player and state[13]==player and state[14]==player:
            return "win"
        if state[15]==player and state[16]==player and state[17]==player:
            return "win"
        if state[16]==player and state[17]==player and state[18]==player:
            return "win"
        if state[17]==player and state[18]==player and state[19]==player:
            return "win"
            
# Horizontal Left wins
        if state[4]==player and state[3]==player and state[2]==player:
            return "win"
        if state[3]==player and state[2]==player and state[1]==player:
            return "win"
        if state[2]==player and state[1]==player and state[0]==player:
            return "win"
        if state[9]==player and state[8]==player and state[7]==player:
            return "win"
        if state[8]==player and state[7]==player and state[6]==player:
            return "win"
        if state[7]==player and state[6]==player and state[5]==player:
            return "win"
        if state[14]==player and state[13]==player and state[12]==player:
            return "win"
        if state[13]==player and state[12]==player and state[11]==player:
            return "win"
        if state[12]==player and state[11]==player and state[10]==player:
            return "win"
        if state[19]==player and state[18]==player and state[17]==player:
            return "win"
        if state[18]==player and state[17]==player and state[16]==player:
            return "win"
        if state[17]==player and state[16]==player and state[15]==player:
            return"win"
            
# Vertical down Wins
        if state[0]==player and state[5]==player and state[10]==player:
            return "win"
        if state[5]==player and state[10]==player and state[15]==player:
            return "win"
        if state[1]==player and state[6]==player and state[11]==player:
            return "win"
        if state[6]==player and state[11]==player and state[16]==player:
            return "win"
        if state[2]==player and state[7]==player and state[12]==player:
            return "win"
        if state[7]==player and state[12]==player and state[17]==player:
            return "win"
        if state[3]==player and state[8]==player and state[13]==player:
            return "win"
        if state[8]==player and state[13]==player and state[18]==player:
            return "win"
        if state[4]==player and state[9]==player and state[14]==player:
            return "win"
        if state[9]==player and state[14]==player and state[19]==player:
            return "win"
            
#vertical up wins
        if state[15]==player and state[10]==player and state[5]==player:
            return "win"
        if state[10]==player and state[5]==player and state[0]==player:
            return "win"
        if state[16]==player and state[11]==player and state[6]==player:
            return"win"
        if state[11]==player and state[6]==player and state[1]==player:
            return"win"
        if state[17]==player and state[12]==player and state[7]==player:
            return "win"
        if state[12]==player and state[7]==player and state[2]==player:
            return "win"
        if state[18]==player and state[13]==player and state[8]==player:
            return "win"
        if state[13]==player and state[8]==player and state[3]==player:
            return"win"
        if state[19]==player and state[14]==player and state[9]==player:
            return "win"
        if state[14]==player and state[9]==player and state[4]==player:
            return "win"
            
#Diagonal up&left
        if state[17]==player and state[11]==player and state[5]==player:
            return "win"
        if state[18]==player and state[12]==player and state[6]==player:
            return"win"
        if state[12]==player and state[6]==player and state[0]==player:
            return "win"
        if state[19]==player and state[13]==player and state[7]==player:
            return "win"
        if state[13]==player and state[7]==player and state[1]==player:
            return "win"
        if state[14]==player and state[8]==player and state[2]==player:
            return "win"
    
# Diagonal up&right
        if state[10]==player and state[6]==player and state[2]==player:
            return "win"
        if state[15]==player and state[11]==player and state[7]==player:
            return "win"
        if state[11]==player and state[7]==player and state[3]==player:
            return "win"
        if state[16]==player and state[12]==player and state[8]==player:
            return "win"
        if state[12]==player and state[8]==player and state[4]==player:
            return "win"
        if state[17]==player and state[13]==player and state[9]==player:
            return "win"
            
# Diagonal down&left 
        if state[2]==player and state[6]==player and state[10]==player:
            return "win"
        if state[3]==player and state[7]==player and state[11]==player:
            return "win"
        if state[7]==player and state[11]==player and state[15]==player:
            return "win"
        if state[4]==player and state[8]==player and state[12]==player:
            return "win"
        if state[8]==player and state[12]==player and state[16]==player:
            return "win"
        if state[9]==player and state[13]==player and state[17]==player:
            return "win"
            
# Diagonal down&right
        if state[5]==player and state[11]==player and state[17]==player:
            return "win"
        if state[0]==player and state[6]==player and state[12]==player:
            return "win"
        if state[6]==player and state[12]==player and state[18]==player:
            return "win"
        if state[1]==player and state[7]==player and state[13]==player:
            return "win"
        if state[7]==player and state[13]==player and state[19]==player:
            return "win"
        if state[2]==player and state[8]==player and state[14]==player:
            return "win"
        return None


# In[8]:


def human_move(state,player):
    print("Locations:")
    state.show_locations()
    print("Valid Moves:")
    print(valid_moves(state,player))
    
    while True:
        move=eval(input("Enter your move"))

        if move not in valid_moves(state,player):
            print("That is not a valid move")
        else:
            break
    
    return move

human_agent=Agent(human_move)


# In[9]:


def show_state(state,player):
    print(state)


# In[10]:


def monkey_move(state,player):
    return random.choice(valid_moves(state,player))
monkey_agent=Agent(monkey_move)


# In[11]:


from Game.minimax import *
def minimax_move(state,player):
    values,actions=minimax_values(state,player,display=False,maxdepth=12)
    return top_choice(actions,values)
minimax_agent=Agent(minimax_move)
     


# In[12]:


def heuristic(state,player):
    return -1


# # (4,5) board with 4 open spots at the top

# In[13]:


state=Board(4,5)
for loc in [0,6,8,10,11,13,14,17]:
    state[loc]=1
for loc in [5,7,9,12,15,16,18,19]:
    state[loc]=2
state


# In[14]:


minimax_values(state,player=1)


# In[15]:


plot_minimax_tree(state,1)


# In[16]:


class Node():

    def __init__(self,value,m=5,h=10):
        self.value=value
        self.children=[]
        self.parent=None
        self.x=0
        self.y=0
        self.abs_xy=None
        self.ext=[-m,m]
        self.m=m
        self.h=h

    def __iadd__(self,y):
        try:
            for item in y:
                self.children.append(item)
                item.parent=self
        except TypeError:
            self.children.append(y)

        return self


# In[17]:


def get_xy(node):
    import numpy as np
    
    if node.abs_xy is None:
        adjust_extents(node)
    x=[]
    y=[]
    labels=[]
     
    def _traverse(node,parent_x=0,depth=0):
        node.abs_xy=[node.x+parent_x,-node.y]
        x.append(node.x+parent_x)
        y.append(-node.y)
        labels.append(str(node.value)[:-1])
        for child in node.children:
            _traverse(child,node.x+parent_x,depth+1)
            
    _traverse(node)   

    return np.array(x),np.array(y),labels


# In[18]:


def adjust_extents(node,depth=0):

    node.y=node.h*depth

    if not node.children:
        node.x=0
        node.ext=[-node.m,node.m]
        return

    for c in node.children:
        adjust_extents(c,depth+1)    

    cdf=0
    for c in node.children:
        df=c.ext[1]-c.ext[0]
        c.x=cdf+df/2
        cdf+=df

    for c in node.children:
        c.x-=cdf/2

    node.ext=[-cdf/2,+cdf/2]


# In[19]:


def get_lines(node):
    import numpy as np
    if node.abs_xy is None:
        adjust_extents(node)

    x=[]
    y=[]

    def _traverse(node,parent_x=0,depth=0):        
        for child in node.children:
            x.append([node.abs_xy[0]])
            y.append([node.abs_xy[1]])
            x.append([child.abs_xy[0]])
            y.append([child.abs_xy[1]])
            x.append([np.nan])
            y.append([np.nan])

            _traverse(child)
    _traverse(node)            

    return np.array(x),np.array(y)
    


# In[20]:


def tree(current_state,player,depth=0,maxdepth=inf,m=5,h=10):

    node=Node(deepcopy(current_state),m=m,h=h)
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return 
    
    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for min
        return node
    elif status=='lose':  # good for min
        return node
    elif status=='stalemate':  # draw
        return node


    moves=valid_moves(current_state,player)
    if moves is None:
        raise ValueError("valid_moves returned None with state=%s and player=%d - Did you forget to return the moves?" % (str(current_state),player))
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    
    for state in available_states:
        node+=tree(state,other_player,depth+1,maxdepth,m=m,h=h)

    return node
    


# In[43]:


state=Board(4,5)
for loc in [0,6,8,10,11,13,14,17]:
    state[loc]=1
for loc in [5,7,9,12,15,16,18,19]:
    state[loc]=2
state


# In[44]:


node=tree(state,1)
x,y,labels=get_xy(node)
xl,yl=get_lines(node)
figure(figsize=(20,8))
plot(xl,yl,'k-')
plot(x,y,'o',color='white',markeredgecolor='black',markersize=60, clip_on=False)
for xx,yy,L in zip(x,y,labels):
    text(xx,yy,L,ha='center',va='center',color='black',fontfamily='monospace')
xl=gca().get_xlim()
yl=gca().get_ylim()
gca().set_ylim([yl[0]-2,yl[1]+2])
axis('off')


# In[45]:


figure(figsize=(80,32))
node=tree(state,1,m=60,h=130)
x,y,labels=get_xy(node)
xl,yl=get_lines(node)
figure(figsize=(20,8))
plot(xl,yl,'k-', zorder=1)

for xx,yy in zip(x,y):
    h=Circle((xx,yy),50,facecolor='white',edgecolor='black', zorder=2)
    gca().add_artist(h)
# #plot(x,y,'o',color='white',markeredgecolor='black',markersize=60, clip_on=False)
for xx,yy,L in zip(x,y,labels):
    text(xx,yy,L,ha='center',va='center',color='black',fontfamily='monospace',size=5)
xl=gca().get_xlim()
yl=gca().get_ylim()
#axis('off')
axis('equal');
gca().set_ylim([yl[0]-20,yl[1]+20])


# In[ ]:




