class Node():

    def __init__(self,value,m=50,h=100):
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


def get_lines2(node):
    import numpy as np
    if node.abs_xy is None:
        adjust_extents(node)

    x=[]
    y=[]

    def _traverse(node,parent_x=0,depth=0):        
        for child in node.children:
            x.append([node.abs_xy[0],child.abs_xy[0]])
            y.append([node.abs_xy[1],child.abs_xy[1]])

            _traverse(child)
    _traverse(node)            

    return np.array(x),np.array(y)
    

def tree(current_state,player,depth=0,maxdepth=inf,m=50,h=100):

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
    

def draw_tree(state,maxdepth=inf)

    from drawio import *

    node=tree(state,1,m=50,h=200,maxdepth=maxdepth)
    x,y,labels=get_xy(node)
    xl,yl=get_lines2(node)
    width=max(x)+30
    height=max(y)+30

    d = drawio(width, height)

    for xx,yy in zip(xl,yl):
        d.line(xx[0], height-yy[0],xx[1],height-yy[1],strokeColor='black')

    for xx,yy,L in zip(x,y,labels):
        d.circle(xx,height-yy,node.m//2,text=state2text(state))

