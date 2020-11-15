from copy import deepcopy
import inspect
import datetime

def repeat_move_default(*args,**kwargs):
    return False

def mcts_values(current_state,player,T,seconds=30,max_moves=100):
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

    
    
    moves=valid_moves(current_state,player)
    if len(moves)==1:
        return [[1.0],moves]
    

    original_state=deepcopy(current_state)
    
    #T=Table()
    
    calculation_time=datetime.timedelta(seconds=seconds)
    
    begin=datetime.datetime.utcnow()
    
    games=0
    while datetime.datetime.utcnow()-begin< calculation_time:
        mcts_run_simulation(current_state,player,max_moves,T)
        games+=1
        
    
    available_states=[update_state(deepcopy(current_state),player,move)
                                    for move in moves]    


    for S in available_states:
        if (S,player) not in T:
            T[(S,player)]={'wins':0,'plays':1}

    # percent_wins,move=max(
    #     (T[(S,player)]['wins']/T[(S,player)]['plays'],
    #      move) for S,move in zip(available_states,moves)
    # )
    
    
    values=[float(T[(S,player)]['wins'])/T[(S,player)]['plays'] for S in available_states]
    
    # sort by value
    values,moves=mysort(values,moves,reverse=True)

    
    return values,moves
    

from math import log, sqrt
def mysort(*args,**kwargs):

    reverse=kwargs.get('reverse',False)
    b=sorted(zip(*args),reverse=reverse)

    newargs=[]
    for i in range(len(args)):
        newargs.append([x[i] for x in b])
        
    return newargs

def argmax(v):

    y=list(zip(v,list(range(len(v)))))
    return max(y)[1]


def top_choice(choices,weights=None):

    if isinstance(choices,dict):  # given a dictionary
        Q=choices
        choices=[]
        weights=[]
        for key in list(Q.keys()):
            if isinstance(key,tuple):
                choices.append(list(key))
            else:
                choices.append(key)
            weights.append(Q[key])

    i=argmax(weights)
    return choices[i]

def mcts_run_simulation(state,player,max_moves,T):
    import random
    from Game.tables import make_immutable

    visited_state_player=[]
    original_player=player
    
    C=1.4  # what is this?
    
    if player==1:
        other_player=2
    else:
        other_player=1
    
    
    first_time=True
    for t in range(max_moves):
        state=deepcopy(state)
        
        moves=valid_moves(state,player)

        if moves==[]:
            raise ValueError("State\n%s has no moves for player %d" % (str(state),player))


        available_states=[update_state(deepcopy(state),player,move)
                                        for move in moves]    
        available_states=[make_immutable(S) for S in available_states]

        if all( [(S,player) in T for S in available_states] ):

            plays=[T[(S,player)]['plays'] for S in available_states]
            wins=[T[(S,player)]['wins'] for S in available_states]
            
            if not sum(plays):
                print([T[(S,player)] for S in available_states])


            if not all(plays):
                print([T[(S,player)] for S in available_states])

            log_total = log(sum(plays))
            values=[w/p+C*sqrt(log_total/p) for w,p in zip(wins,plays)]
            values,moves=mysort(values,moves,reverse=True)
            
            move=top_choice(moves,values)
        else:
            move=random.choice(moves)
        
        
        
        state=update_state(state,player,move)
        status=win_status(state,player)
        
        # note - this is the state *after* the move by player
        visited_state_player.append((state,player))
        if first_time and not (state,player) in T:  # not sure why only the first time this call
            T[(state,player)]={'plays':1,'wins':0}
            first_time=False
        
        if not status is None:  # end game
            break
            
        player,other_player=other_player,player
        
    if status=='win':
        winner=player
    elif status=='lose':
        winner=other_player
    else:
        winner=None
        
    for state,player in visited_state_player:
        if (state,player) not in T:
            continue
            
        T[(state,player)]['plays']+=1
        if player==winner:
            T[(state,player)]['wins']+=1
            
        