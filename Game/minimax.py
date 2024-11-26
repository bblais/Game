inf=1e500
import inspect
import time
from copy import deepcopy
from functools import lru_cache

from typing import Callable, TypeVar, Any
from typing_extensions import ParamSpec

from functools import lru_cache, _CacheInfo

def hash_list(l: list) -> int:
    __hash = 0
    for i, e in enumerate(l):
        __hash = hash((__hash, i, hash_item(e)))
    return __hash

def hash_dict(d: dict) -> int:
    __hash = 0
    for k, v in d.items():
        __hash = hash((__hash, k, hash_item(v)))
    return __hash

def hash_item(e) -> int:
    if hasattr(e, '__hash__') and callable(e.__hash__):
        try:
            return hash(e)
        except TypeError:
            pass
    if isinstance(e, (list, set, tuple)):
        return hash_list(list(e))
    elif isinstance(e, (dict)):
        return hash_dict(e)
    else:
        raise TypeError(f'unhashable type: {e.__class__}')

PT = ParamSpec("PT")
RT = TypeVar("RT")

def lru_cache_ext(*opts, hashfunc: Callable[..., int] = hash_item, **kwopts) -> Callable[[Callable[PT, RT]], Callable[PT, RT]]:
    def decorator(func: Callable[PT, RT]) -> Callable[PT, RT]:
        class _lru_cache_ext_wrapper:
            args: tuple
            kwargs: dict[str, Any]

            def cache_info(self) -> _CacheInfo: ...
            def cache_clear(self) -> None: ...

            @classmethod
            @lru_cache(*opts, **kwopts)
            def cached_func(cls, args_hash: int) -> RT:
                return func(*cls.args, **cls.kwargs)

            @classmethod
            def __call__(cls, *args: PT.args, **kwargs: PT.kwargs) -> RT:
                __hash = hashfunc((id(func), *[hashfunc(a) for a in args], *[(hashfunc(k), hashfunc(v)) for k, v in kwargs.items()]))

                cls.args = args
                cls.kwargs = kwargs

                cls.cache_info = cls.cached_func.cache_info
                cls.cache_clear = cls.cached_func.cache_clear

                return cls.cached_func(__hash)

        return _lru_cache_ext_wrapper()

    return decorator




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
    
@lru_cache_ext(maxsize=None)
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
    
@lru_cache_ext(maxsize=None)
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
    
@lru_cache_ext(maxsize=None)
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
    
@lru_cache_ext(maxsize=None)
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
 

#=============== NOCACHE
def minvalue_ab_nocache(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
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
            payoff=minvalue_ab_nocache(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=maxvalue_ab_nocache(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff<value:
            value=payoff
            b=min([b,value])
            if b<=a:
                return a
        
    if value==inf:  # no available states  = stalemate
        return 0
    else:
        return value
    

def maxvalue_ab_nocache(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
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
            payoff=maxvalue_ab_nocache(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=minvalue_ab_nocache(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff>value:
            value=payoff
            a=max([a,value])
            if a>=b:
                return b
        
        
    if value==-inf:  # no available states  = stalemate
        return 0
    else:
        return value
    

def minvalue_ab_depth_nocache(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
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
            payoff=minvalue_ab_depth_nocache(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=maxvalue_ab_depth_nocache(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff<value:
            value=payoff
            b=min([b,value])
            if b<=a:
                return a
        
    if value==inf:  # no available states  = stalemate
        return 0
    else:
        return value
    

def maxvalue_ab_depth_nocache(current_state,player,depth=0,a=-inf,b=inf,maxdepth=inf,verbose=False):
    
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
            payoff=maxvalue_ab_depth_nocache(state,player,depth+1,a,b,maxdepth,verbose=verbose)
        else:
            payoff=minvalue_ab_depth_nocache(state,other_player,depth+1,a,b,maxdepth,verbose=verbose)

        if payoff>value:
            value=payoff
            a=max([a,value])
            if a>=b:
                return b
        
        
    if value==-inf:  # no available states  = stalemate
        return 0
    else:
        return value
 

#=============== NOCACHE


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

def minimax_reset():
    global valid_moves,win_status,update_state,repeat_move

    d = dir()
    for varname in ['minimax_values','update_state','valid_moves',
                    'initial_state','show_state','win_status']:
        if varname in d:
            print(f"Removing {varname}")
            del globals()[varname]    


def minimax_values(current_state,player,maxdepth=inf,
                adjust_values_by_depth=False,display=True,
                verbose=False,cache=True):

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

    if moves is None:
        print("Valid moves returned no moves for this state:")
        print(state)
        raise ValueError

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
                if cache:
                    value=maxvalue_ab_depth(state,player,maxdepth=maxdepth)
                else:
                    value=maxvalue_ab_depth_nocache(state,player,maxdepth=maxdepth)
            else:
                if cache:
                    value=minvalue_ab_depth(state,other_player,maxdepth=maxdepth,verbose=verbose)
                else:
                    value=minvalue_ab_depth_nocache(state,other_player,maxdepth=maxdepth,verbose=verbose)

            values.append(value)
    else:        
        for state,repeat in zip(available_states,repeats):
            if isinstance(state,list):
                state=List(state)
            if repeat:
                if cache:
                    value=maxvalue_ab(state,player,maxdepth=maxdepth)
                else:
                    value=maxvalue_ab_nocache(state,player,maxdepth=maxdepth)
            else:
                if cache:
                    value=minvalue_ab(state,other_player,maxdepth=maxdepth,verbose=verbose)
                else:
                    value=minvalue_ab_nocache(state,other_player,maxdepth=maxdepth,verbose=verbose)

            values.append(value)

    # sort by value
    values,moves=mysort(values,moves,reverse=True)

    if display:
        print("  Choice Time: %s" % time2str(time.time()-start_time))


    return values,moves


def walk(current_state,player,depth=0,counts={},maxdepth=inf):
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
    
    if player==1:
        other_player=2
    else:
        other_player=1

    if depth in counts:
        counts[depth]+=1
    else:
        counts[depth]=1
        
    if depth>maxdepth:
        return 
    

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if status=='win':  # bad for min
        return
    elif status=='lose':  # good for min
        return
    elif status=='stalemate':  # draw
        return


    moves=valid_moves(current_state,player)
    if moves is None:
        raise ValueError("valid_moves returned None with state=%s and player=%d - Did you forget to return the moves?" % (str(current_state),player))
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    
    values=[]
    for state in available_states:
        walk(state,other_player,depth+1,counts,maxdepth)
        
def node_pos(current_state,player,depth=0,width=1., vert_gap = 0.2, 
             vert_loc = 0, xcenter = 0.5,root=None,
            pos = None, parent = None,connections=[],all_states={}):
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
    
    if player==1:
        other_player=2
    else:
        other_player=1

    # since win_status is called with a player and an updated state
    # the current state is really the updated state from the
    # other player's last move.

    status=win_status(current_state,other_player)
    if not status in ['win','lose','stalemate',None]:
        raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

    if pos is None:
        pos = {0:[xcenter,vert_loc]}
        all_states[0]=current_state
        root=0
    else:
        pos[root] = [xcenter, vert_loc]
        
    if not connections:
        connections=[]
        
        
        
    if status=='win':  # bad for min
        all_states[root]=current_state,True
        return pos,connections,all_states
    elif status=='lose':  # good for min
        all_states[root]=current_state,True
        return pos,connections,all_states
    elif status=='stalemate':  # draw
        all_states[root]=current_state,True
        return pos,connections,all_states
    else:
        all_states[root]=current_state,False

    
    moves=valid_moves(current_state,player)
    if moves is None:
        raise ValueError("valid_moves returned None with state=%s and player=%d - Did you forget to return the moves?" % (str(current_state),player))
    available_states=[update_state(deepcopy(current_state),player,move)
                                for move in moves]
    
    if available_states:
        dx = width/len(available_states) 
        nextx = xcenter - width/2 - dx/2
        for state in available_states:
            nextx += dx
            connections.append( [len(pos),root])
            pos,connections,all_states = node_pos(state,other_player,depth+1, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                pos=pos, parent = root,root=len(pos),connections=connections,all_states=all_states)
    return pos,connections,all_states

def spread(pos):
    level=1
    
    while True:
    
        yl=.1-.2*level,.1-.2*(level+1)
        y=plt.array([pos[key][1] for key in pos])

        keys=list(pos.keys())

        idx=plt.where((y<=yl[0]) & (y>=yl[1]))[0]

        if not len(idx):
            break


        x=plt.array([pos[keys[i]][0] for i in idx])
        y=plt.array([pos[keys[i]][1] for i in idx])

    
        x=plt.linspace(0,1,len(x))
        for i,xx in zip(idx,x):
            key=keys[i]
            pos[key][0]=xx
    
        level+=1
        
def spread2(pos,minx=0.07):
    level=1
    
    while True:
    
        yl=.1-.2*level,.1-.2*(level+1)
        y=plt.array([pos[key][1] for key in pos])

        keys=list(pos.keys())

        idx=plt.where((y<=yl[0]) & (y>=yl[1]))[0]

        if not len(idx):
            break


        x=plt.array([pos[keys[i]][0] for i in idx])
        y=plt.array([pos[keys[i]][1] for i in idx])

        for i in range(1,len(x)):
            dx=minx-(x[i]-x[i-1])
            if dx>0:
                x[i:]=x[i:]+dx
        
        for i,xx in zip(idx,x):
            key=keys[i]
            pos[key][0]=xx
    
        level+=1        

def plot_minimax_tree(state,player,figsize=(30,20),ms=60):
    import pylab as plt

    plt.figure(figsize=figsize)
    pos,conn,states=node_pos(state,2)

    #spread(pos)



    x=plt.array([pos[key][0] for key in pos])
    y=plt.array([pos[key][1] for key in pos])

    for start,end in conn:
        if end is None:
            continue
        x1,y1=pos[start]        
        x2,y2=pos[end]        
        plt.plot([x1,x2],[y1,y2],'k-')

    plt.plot(x,y,'bo',ms=60)


    for key in pos:
        x,y=pos[key]
        depth=int(round(y/-0.2))
        
        if states[key][1]:
            plt.plot(x,y,'mo',ms=ms)
            value=str(maxvalue(states[key][0],2))
            if value=='1':
                value='+1'
            plt.text(x,y-.05,value,color='m',va='center',ha='center',size=20)
        else:
            if depth%2==0:
                value=str(maxvalue(states[key][0],2))
            else:
                value=str(minvalue(states[key][0],1))
            if value=='1':
                value='+1'
            #plt.text(x+.02,y-.05,value,color='b',va='center',ha='center',size=20)
        plt.text(x,y,str(states[key][0]).rstrip('\n'),
                 fontfamily='courier',va='center',ha='center',color='white')

        plt.ylim([-1,.1])
            
