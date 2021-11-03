inf=1e500
import inspect
import time
from copy import deepcopy
from functools import lru_cache

class List(list):

    def immutable(self):
        return tuple(self)

    def __hash__(self):
        return hash(tuple(self))

def bad_heuristic(current_state,player):
    return 0
    
def minimax_heuristic(current_state,player):
    global heuristic
        
    try:
        if heuristic:
            pass
    except NameError:
        f=inspect.currentframe()
        out=inspect.getouterframes(f)
        
        parent_dict=None
        for oo in out:
            dd=oo[0].f_locals
            if 'heuristic' in dd:
                parent_dict=dd


        if parent_dict:        
            heuristic=parent_dict['heuristic']
        else:
            heuristic=bad_heuristic

    return heuristic(current_state,player)

def minvalue(current_state,player,depth=0,maxdepth=inf):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)
    

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for min
        return 1
    elif status=='lose':  # good for min
        return -1
    elif status=='stalemate':  # draw
        return 0


    moves=valid_moves(current_state,player)
    if moves is None:
        raise ValueError("valid_moves returned None with state=%s and player=%d - Did you forget to return the moves?" % (str(current_state),player))
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) 
        for move in moves]
    
    values=[]
    for state,repeat in zip(available_states,repeats):
        if repeat:
            value=minvalue(state,player,depth+1,maxdepth)
        else:
            value=maxvalue(state,other_player,depth+1,maxdepth)
        values.append(value)
        
        
    if not values:  # no available states  = stalemate
        return 0
    else:
        return min(values)
    
def maxvalue(current_state,player,depth=0,maxdepth=inf):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for max
        return -1
    elif status=='lose':  # good for max
        return 1
    elif status=='stalemate':  # draw
        return 0

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) for move in moves]
    
    values=[]
    for state,repeat in zip(available_states,repeats):
        if repeat:
            value=maxvalue(state,player,depth+1,maxdepth)
        else:
            value=minvalue(state,other_player,depth+1,maxdepth)
        values.append(value)
        
    if not values:  # no available states  = stalemate
        return 0
    else:
        return max(values)
    
@lru_cache(maxsize=None)
def minvalue_ab(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)

    if verbose:
        tabs='\t'*depth
        print(tabs,"MIN value current state %d\n" % depth)
        s=current_state
        print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for min
        if verbose:
            print(tabs,"end state value: 1")

        return 1
    elif status=='lose':  # good for min
        if verbose:
            print(tabs,"end state value: -1")

        return -1
    elif status=='stalemate':  # draw
        if verbose:
            print(tabs,"end state value: 0")

        return 0

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) for move in moves]
    
    if verbose:
        print(tabs,"Getting MAX value for states")
        for s in available_states:
            print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    


    value=inf
    for state,repeat in zip(available_states,repeats):
        if repeat:
            payoff=minvalue_ab(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=maxvalue_ab(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff<value:
            value=payoff
            b=min([b,value])
            if b<=a:
                return a
        
    if value==inf:  # no available states  = stalemate
        return 0
    else:
        return value
    
@lru_cache(maxsize=None)
def maxvalue_ab(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)

    if verbose:
        tabs='\t'*depth
        print(tabs,"MAX value current state %d\n" % depth)
        s=current_state
        print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    


    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for max
        if verbose:
            print(tabs,"end state value: -1")
        return -1
    elif status=='lose':  # good for max
        if verbose:
            print(tabs,"end state value: 1")
        return 1
    elif status=='stalemate':  # draw
        if verbose:
            print(tabs,"end state value: 0")
        return 0

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) for move in moves]
    
    if verbose:
        print(tabs,"Getting MIN value for states")
        for s in available_states:
            print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    


    value=-inf
    for state,repeat in zip(available_states,repeats):
        if repeat:
            payoff=maxvalue_ab(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=minvalue_ab(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff>value:
            value=payoff
            a=max([a,value])
            if a>=b:
                return b
        
        
    if value==-inf:  # no available states  = stalemate
        return 0
    else:
        return value
    
@lru_cache(maxsize=None)
def minvalue_ab_depth(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)+depth/1000.0

    if verbose:
        tabs='\t'*depth
        print(tabs,"MIN value current state\n")
        s=current_state
        print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for min
        if verbose:
            print(tabs,"end state value: 1 - %d/1000 = %f" % (depth,1-depth/1000.0))

        return 1-depth/1000.0
    elif status=='lose':  # good for min
        if verbose:
            print(tabs,"end state value: -1 + %d/1000 = %f" % (depth,-1+depth/1000.0))
        return -1+depth/1000.0
    elif status=='stalemate':  # draw
        if verbose:
            print(tabs,"end state value: 0 + %d/1000 = %f" % (depth,0+depth/1000.0))
        return 0+depth/1000.0

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) for move in moves]

    if verbose:
        print(tabs,"Getting MAX value for states")
        for s in available_states:
            print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    


    value=inf
    for state,repeat in zip(available_states,repeats):
        if repeat:
            payoff=minvalue_ab_depth(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=maxvalue_ab_depth(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff<value:
            value=payoff
            b=min([b,value])
            if b<=a:
                return a
        
    if value==inf:  # no available states  = stalemate
        return 0
    else:
        return value
    
@lru_cache(maxsize=None)
def maxvalue_ab_depth(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth>maxdepth:
        return minimax_heuristic(current_state,player)-depth/1000.0

    if verbose:
        tabs='\t'*depth
        print(tabs,"MAX value current state\n")
        s=current_state
        print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for max
        if verbose:
            print(tabs,"end state value: -1 + %d/1000 = %f" % (depth,-1+depth/1000.0))

        return -1+depth/1000.0
    elif status=='lose':  # good for max
        if verbose:
            print(tabs,"end state value: 1 - %d/1000 = %f" % (depth,1-depth/1000.0))
        return 1-depth/1000.0
    elif status=='stalemate':  # draw
        if verbose:
            print(tabs,"end state value: 0 - %d/1000 = %f" % (depth,0-depth/1000.0))

        return 0-depth/1000.0

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) for move in moves]
    
    if verbose:
        print(tabs,"Getting MIN value for states")
        for s in available_states:
            print('\n'.join([tabs +_ for _ in str(s).split('\n')]))    


    value=-inf
    for state,repeat in zip(available_states,repeats):
        if repeat:
            payoff=maxvalue_ab_depth(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=minvalue_ab_depth(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff>value:
            value=payoff
            a=max([a,value])
            if a>=b:
                return b
        
        
    if value==-inf:  # no available states  = stalemate
        return 0
    else:
        return value
 
def mysort(*args,**kwargs):

    reverse=kwargs.get('reverse',False)
    b=sorted(zip(*args),reverse=reverse)
    
    newargs=[]
    for i in range(len(args)):
        newargs.append([x[i] for x in b])
        
    return newargs

def time2str(t):

    minutes=60
    hours=60*minutes
    days=24*hours
    years=365*days
    
    yr=int(t/years)
    t-=yr*years

    dy=int(t/days)
    t-=dy*days
    
    hr=int(t/hours)
    t-=hr*hours

    mn=int(t/minutes)
    t-=mn*minutes

    sec=t

    s=""
    if yr>0:
        s+=str(yr)+" years "
    if dy>0:
        s+=str(dy)+" days "
    if hr>0:
        s+=str(hr)+" hours "
    if mn>0:
        s+=str(mn)+" minutes "        
        
    s+=str(sec)+" seconds "


    return s


def minimax_values_orig(current_state,player,maxdepth=inf,display=True):

    global valid_moves,win_status,update_state,repeat_move
    
    try:
        if valid_moves:
            pass
    except NameError:
        f=inspect.currentframe()
        out=inspect.getouterframes(f)
        
        parent_dict=None
        for oo in out:
            dd=oo[0].f_locals
            if 'valid_moves' in dd:
                parent_dict=dd

#        parent_dict=out[3][0].f_locals
        
        valid_moves=parent_dict['valid_moves']
        update_state=parent_dict['update_state']
        try:
            repeat_move=parent_dict['repeat_move']
        except KeyError:
            repeat_move=repeat_move_default
        win_status=parent_dict['win_status']


    start_time=time.time()

    if player==1:
        other_player=2
    else:
        other_player=1

    values=[]
    states=[]

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    repeats=[repeat_move(deepcopy(current_state),player,move) 
                for move in moves]
    
    for state,repeat in zip(available_states,repeats):
        if repeat:
            value=maxvalue(state,player,maxdepth=maxdepth)
        else:
            value=minvalue(state,other_player,maxdepth=maxdepth)
        values.append(value)
        states.append(state)
        

    # sort by value
    values,moves=mysort(values,moves,reverse=True)

    if display:
        print("  Choice Time: %s" % time2str(time.time()-start_time))


    return values,moves

def repeat_move_default(*args,**kwargs):
    return False

def minimax_values(current_state,player,maxdepth=inf,
                adjust_values_by_depth=False,display=True,verbose=False):

    global valid_moves,win_status,update_state,repeat_move
    
    try:
        if valid_moves:
            pass
    except NameError:
        f=inspect.currentframe()
        out=inspect.getouterframes(f)
        
        parent_dict=None
        for oo in out:
            dd=oo[0].f_locals
            if 'valid_moves' in dd:
                parent_dict=dd

#        parent_dict=out[3][0].f_locals
        
        valid_moves=parent_dict['valid_moves']
        update_state=parent_dict['update_state']
        win_status=parent_dict['win_status']
        try:
            repeat_move=parent_dict['repeat_move']
        except KeyError:
            repeat_move=repeat_move_default


    start_time=time.time()

    if player==1:
        other_player=2
    else:
        other_player=1

    values=[]
    states=[]

    moves=valid_moves(current_state,player)
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]

    if verbose:
        print("minimax_values verbose current state\n")
        print(current_state)
        print("Getting MIN value for states")
        for s in available_states:
            print(s)



    repeats=[repeat_move(deepcopy(current_state),player,move) 
                for move in moves]
    
    if adjust_values_by_depth:
        for state,repeat in zip(available_states,repeats):
            if isinstance(state,list):
                state=List(state)

            if repeat:
                value=maxvalue_ab_depth(state,player,maxdepth=maxdepth)
            else:
                value=minvalue_ab_depth(state,other_player,maxdepth=maxdepth,verbose=verbose)
            values.append(value)
    else:        
        for state,repeat in zip(available_states,repeats):
            if isinstance(state,list):
                state=List(state)
            if repeat:
                value=maxvalue_ab(state,player,maxdepth=maxdepth)
            else:
                value=minvalue_ab(state,other_player,maxdepth=maxdepth,verbose=verbose)
            values.append(value)

    # sort by value
    values,moves=mysort(values,moves,reverse=True)

    if display:
        print("  Choice Time: %s" % time2str(time.time()-start_time))


    return values,moves




