#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from pylab import *
from Game import *
from Game.minimax import *
inf=1e500


# In[2]:


def initial_state():
    state=Board(3,3)
    state.pieces=['.','X','O']
    # state[0]=1 in cases where we need to have starting pieces
    return state


# In[3]:


def valid_moves(state,player):
    
    # nope -- return [0,1,2,3,4,5,6,7,8]
    
    EMPTY=0
    X=1
    O=2
    
    moves=[]
    
    if state[0]==0:
        moves.append(0)
    if state[1]==0:
        moves.append(1)        
    if state[2]==0:
        moves.append(2)
        
    #....
    
    moves=[]
    for location in range(9):
        if state[location]==EMPTY:
            moves.append(location)
    
    
    return moves


# In[4]:


def update_state(state,player,move):
    
    new_state=state
    
    new_state[move]=player
    
    return new_state


# In[5]:


def three_in_a_row(a,b,c,player):
    
    if a==player and b==player and c==player:
        return True
    else:
        return False
    
    
    
def win_status(state,player):
    
    # 0 1 2
    # 3 4 5
    # 6 7 8
    
    if player==1:
        other_player=2
    else:
        other_player=1
    
    if three_in_a_row(state[0],state[1],state[2],player):
        return 'win'
    if three_in_a_row(state[3],state[4],state[5],player):
        return 'win'
    if three_in_a_row(state[6],state[7],state[8],player):
        return 'win'
    if three_in_a_row(state[0],state[3],state[6],player):
        return 'win'
    if three_in_a_row(state[1],state[4],state[7],player):
        return 'win'
    if three_in_a_row(state[2],state[5],state[8],player):
        return 'win'
    if three_in_a_row(state[0],state[4],state[8],player):
        return 'win'
    if three_in_a_row(state[2],state[4],state[6],player):
        return 'win'
    
    if not valid_moves(state,other_player):
        return 'stalemate'
    
    
def show_state(state):
    print(state)
    
    


# In[6]:


# In[3]:


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


# In[4]:


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


# In[5]:


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


# In[6]:


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
    


# In[7]:


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
    


# In[8]:


state=Board(3,3)
for loc in [0,7,8]:
    state[loc]=2
for loc in [2,3,6]:
    state[loc]=1
#state.pieces=['.','X','O']
state


# In[9]:


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


# In[10]:


state=Board(3,3)
for loc in [0,7]:
    state[loc]=2
for loc in [2,3,6]:
    state[loc]=1
#state.pieces=['.','X','O']
state


# In[11]:


node=tree(state,2,m=30)
x,y,labels=get_xy(node)
xl,yl=get_lines(node)

fig_width=(node.ext[1]-node.ext[0])//30
fig_height=(max(y)-min(y))//2

figure(figsize=(fig_width,fig_height))
plot(xl,yl,'k-')
plot(x,y,'o',color='white',markeredgecolor='black',markersize=60, clip_on=False)
for xx,yy,L in zip(x,y,labels):
    text(xx,yy,L,ha='center',va='center',color='black',fontfamily='monospace')
xl=gca().get_xlim()
yl=gca().get_ylim()
gca().set_ylim([yl[0]-2,yl[1]+2])
axis('off')
savefig('tree.pdf')


# In[19]:


state=Board(3,3)
for loc in [0,7]:
    state[loc]=2
for loc in [3,6]:
    state[loc]=1
#state.pieces=['.','X','O']
show_state(state)


node=tree(state,1,m=30)
x,y,labels=get_xy(node)
xl,yl=get_lines(node)

fig_width=(node.ext[1]-node.ext[0])//30
fig_height=(max(y)-min(y))//2

figure(figsize=(fig_width,fig_height))
plot(xl,yl,'k-')
plot(x,y,'o',color='white',markeredgecolor='black',markersize=60, clip_on=False)
for xx,yy,L in zip(x,y,labels):
    text(xx,yy,L,ha='center',va='center',color='black',fontfamily='monospace')
xl=gca().get_xlim()
yl=gca().get_ylim()
gca().set_ylim([yl[0]-2,yl[1]+2])
axis('off')
savefig('tree.pdf')


# In[12]:


plot_minimax_tree(state,2)


# In[13]:


max(y)-min(y)


# In[14]:


fig_height


# In[15]:


fig_width


# In[ ]:




