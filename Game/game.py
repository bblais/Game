import inspect
import random
from copy import deepcopy
from copy import deepcopy as copy
import sys

#from .Memory import Remember as Remember2
#from .Memory import Remember
import os

from random import randint


class Storage(object):
    def __init__(self):
        self.data=[]
    
    def __add__(self,other):
        s=Storage()
        s+=other
        return s
        
    def __iadd__(self,other):
        try:
            self.append(*other)
        except TypeError: # non-iterable
            self.append(other)
        return self
        
    def append(self,*args):
        if not self.data:
            for arg in args:
                self.data.append([arg])

        else:
            for d,a in zip(self.data,args):
                d.append(a)
       
    def arrays(self):
        from numpy import array
        for i in range(len(self.data)):
            self.data[i]=array(self.data[i])

        ret=tuple(self.data)
        if len(ret)==1:
            return ret[0]
        else:
            return ret

    def __array__(self):
        from numpy import vstack
        return vstack(self.arrays())


def sortedby(L,values,reverse=False):

    data=list(zip(values,L))
    data.sort(reverse=reverse)
    
    new_L=[x[1] for x in data]
    return new_L



def gui_input(prompt=''):
    import tkinter.simpledialog
    val=tkinter.simpledialog.askstring('Input', prompt)
    if not val:
        return ''
    else:
        return eval(val)



def _print(*args):
    print(" ".join([str(x) for x in args]))

    


class Struct(dict):
    
    def __getattr__(self,name):
        
        try:
            val=self[name]
        except KeyError:
            val=super(Struct,self).__getattribute__(name)
            
        return val
    
    def __setattr__(self,name,val):
        
        self[name]=val

def no_update(observation,action,reward,done,memory):
    return
    

class Agent(object):
    
    def __init__(self,move,*args,**kwargs):
        
        self.stuff=dict(*args,**kwargs)
        self.stuff['move']=move
        if 'update' not in self.stuff:
            self.stuff['update']=no_update
        if 'memory' not in self.stuff:
            self.stuff['memory']=Struct()
        
        self._initialized=True
        
    def __getitem__(self,key):
        
        return self.stuff[key]
        
    def __setitem__(self,key,val):
        self.stuff[key]=val
        
    def __setattr__(self,item,value):

        if '_initialized' not in self.__dict__:  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        else:
            self.stuff[item]=value
            return

    def __getattr__(self,name):
        # this is called when things fail
        return self.stuff[name]
    
    def __next__(self):
        return next(self.stuff)
        
    def __iter__(self):
        return self.stuff.__iter__()
        
    def __repr__(self):
        
        return str(self.stuff)
 
def all_zero(mylist):

    return len([x for x in mylist if x==0])==len(mylist)
 
def default_repeat_move(*args,**kwargs):
    return False
    
def default_state_to_observation(state,player):
    return state

class Game(object):
    
    def __init__(self,number_of_games=1,**kwargs):
        
        self.display=True
        self.state=None
        self.params=kwargs
        
        self.number_of_games=number_of_games
        self.wins=[]
        
        self.check_repeated_states=False
        self.save_states=False
        
        self.games=[]

        f=inspect.currentframe()
        out=inspect.getouterframes(f)
        self.parent_dict=out[1][0].f_locals
        self.user_funcs=['valid_moves','show_state','initial_state',
                        'update_state','win_status','repeat_move']
        
        #self.register_functions()
        
    def available_states(self,state,player):
        
        states=[]
        observation=self.state_to_observation(state,player)
        for move in self.valid_moves(observation,player):
            newstate=self.update_state(deepcopy(state),player,move)
            if newstate is None:
                raise ValueError("update_state returned None with state=%s and player=%d - Did you forget to return the state?" % (str(state),player))
            states.append(newstate)
            
        return states
        
        
    def state_to_observation(self,state,player):
        if 'state_to_observation' in self.parent_dict:
            s2o=self.parent_dict['state_to_observation']
            observation=s2o(state,player)
        else:
            observation=state

        return observation

        
    def initial_state(self):
        if 'initial_state' in self.parent_dict:
            init=self.parent_dict['initial_state']
            self.state=init(**self.params)
            
        return self.state
        
    def __getattr__(self,name):
        # this is called when things fail
        
        if name in self.user_funcs and name in self.parent_dict:
            return self.parent_dict[name]
        elif name=='repeat_move':  # use a default if not defined
            return default_repeat_move
        else:
            raise AttributeError(name)
            
    def is_valid_move(self,player,move):
        observation=self.state_to_observation(self.state,player)
        moves=self.valid_moves(observation,player)
        try:
            list_move=list(move)  # deal with tuples
            return move in moves or list_move in moves
        except TypeError:
            return move in moves
        
    def report(self):
        wins=self.wins
        N_tie=wins.count(0)
        N_win=wins.count(1)
        N_lose=wins.count(2)+wins.count(3)
        N_autolose=wins.count(3)
        N_games=len(wins)
        print("Total number of games: ",N_games)
        print("Winning %.2f percent" % (100.0*N_win/N_games))
        print("Losing %.2f percent" % (100.0*N_lose/N_games))
        print("Tie %.2f percent" % (100.0*N_tie/N_games))
        if N_autolose:
            print("Illegal Moves Causing Loss %.2f percent" % (100.0*N_autolose/N_games))

    def percent_win_lose_tie(self):
        wins=self.wins
        N_tie=wins.count(0)
        N_win=wins.count(1)
        N_lose=wins.count(2)+wins.count(3)
        N_autolose=wins.count(3)
        N_games=len(wins)

        return 100.0*N_win/N_games,100.0*(N_lose+N_autolose)/N_games,100.0*N_tie/N_games


    def run(self,agent1,agent2):

        self.wins=[]
        for game in range(self.number_of_games):

            if self.display:
                _print("====")
                _print("Game ",game+1)
            self.state=self.initial_state()
            

            if self.save_states:
                game_dict={}
                self.games.append(game_dict)
                game_dict['states']=[deepcopy(self.state)]
                game_dict['moves']=[]
                game_dict['players']=[]


            player,other_player=1,2
            agents=[None,agent1,agent2]  # make a 1-index list

            visited_states={1:[],2:[]}
    

            for agent in agents[1:]:
                agent.states=[]
                agent.actions=[]
                agent.last_action=None
                agent.last_state=None
                agent.last_player=None
                arginfo=inspect.getargspec(agent.move)
                agent.move_args=len(arginfo.args)
            
            move_count=1
            
            while True:
                agents[player].move_count=move_count

                if move_count==player:  # first move
                    try:
                        observation=self.state_to_observation(self.state,player)
                        agents[player].pre(observation,agents[player])
                    except (AttributeError,KeyError):
                        pass


                valid_move=False
                count=0
                auto_lose=False
                
                while not valid_move:
                    observation=self.state_to_observation(self.state,player)

                    if self.display:
                        self.show_state(observation)

                    moves=self.valid_moves(observation,player)
                    if moves==[]:
                        raise ValueError("State %s has no moves for player %d" % (str(self.state),player))

                    if agents[player].move_args==3:
                        move=agents[player].move(observation,player,agents[player])
                    else:
                        move=agents[player].move(observation,player)
                        
                    if move =='':
                        raise ValueError("Empty move quits. ")
                        
                    if self.display:
                        _print("Player %d moves %s" % (player,str(move)))
                        
                    valid_move=self.is_valid_move(player,move)
                    if not valid_move:
                        if self.display:
                            _print("Illegal move by the agent %s: %s.  Automatic Loss." % (str(agents[player]),str(move)))

                        valid_move=True
                        auto_lose=True

                move_count+=1
                agents[player].states.append(deepcopy(observation))
                agents[player].actions.append(deepcopy(move))
                agents[player].last_action=deepcopy(move)
                agents[player].last_state=deepcopy(observation)
                agents[player].last_player=player

                if auto_lose:
                    status='lose'
                    break

                visited_states[player].append(deepcopy(self.state))
                
                new_state=self.update_state(deepcopy(self.state),player,move)
                if new_state is None:
                    raise ValueError("update_state returned None - Did you forget to return the state?")
                repeat=self.repeat_move(deepcopy(new_state),player,move)

                self.state=new_state
                if self.save_states:
                    game_dict['states'].append(deepcopy(self.state))
                    game_dict['moves'].append(deepcopy(move))
                    game_dict['players'].append(player)


                status=self.win_status(self.state,player)

                if not status in ['win','lose','stalemate','tie',None]:
                    raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % str(status))




                if status:
                    break
                elif not self.check_repeated_states:
                    pass
                elif any([self.state==x for x in visited_states[other_player]]):
                    # give your opponent a repeated state and you lose
                    status='lose'
                    break

                if repeat:
                    continue
                
                player,other_player=other_player,player

            if self.display:
                observation=self.state_to_observation(self.state,player)
                self.show_state(observation)

                
            stati=[None,None,None]
            if status=='win':
                if self.display:
                    _print("Player ",player,"won.")
                self.wins.append(player)

                stati[player]='win'
                stati[other_player]='lose'

            elif status=='lose':
                if self.display:
                    _print("Player ",other_player,"won.")
                if auto_lose:
                    self.wins.append(3)
                else:
                    self.wins.append(other_player)
                stati[player]='lose'
                stati[other_player]='win'
            else: # stalemate
                if self.display:
                    _print("Neither player won: ",status)
                self.wins.append(0)
                stati[player]='stalemate'
                stati[other_player]='stalemate'

            try:
                agent1.post(stati[1],1,agent1)
            except (AttributeError,KeyError):
                pass
                
            try:
                agent2.post(stati[2],2,agent2)
            except (AttributeError,KeyError):
                pass

        return self.wins

class CardGame(object):
    
    def __init__(self,number_of_games=1,display=True,**kwargs):
        
        self.display=display
        self.state=None
        self.params=kwargs
        
        self.number_of_games=number_of_games
        self.wins=[]
        
        self.save_states=False
        
        self.games=[]

        f=inspect.currentframe()
        out=inspect.getouterframes(f)
        self.parent_dict=out[1][0].f_locals
        self.user_funcs=['valid_moves','show_state','initial_state',
                        'update_state','win_status','repeat_move']
        
        #self.register_functions()
        
    def available_states(self,state,player):
        
        states=[]
        for move in self.valid_moves(state,player):
            states.append(self.update_state(deepcopy(state),player,move))
            
        return states
        
        
    def initial_state(self):
        if 'initial_state' in self.parent_dict:
            init=self.parent_dict['initial_state']
            self.state=init(agents,**self.params)
            
        return self.state
        
    def __getattr__(self,name):
        # this is called when things fail
        
        if name in self.user_funcs and name in self.parent_dict:
            return self.parent_dict[name]
        elif name=='repeat_move':  # use a default if not defined
            return default_repeat_move
        else:
            raise AttributeError(name)
            
    def is_valid_move(self,player,move):
        moves=self.valid_moves(self.state,player)
        try:
            list_move=list(move)  # deal with tuples
            return move in moves or list_move in moves
        except TypeError:
            return move in moves
        
    def report(self):
        wins=self.wins
        N_tie=wins.count(0)
        N_win=wins.count(1)
        N_lose=wins.count(2)
        N_games=len(wins)
        print("Total number of games: ",N_games)
        print("Winning %.2f percent" % (100.0*N_win/N_games))
        print("Losing %.2f percent" % (100.0*N_lose/N_games))
        print("Tie %.2f percent" % (100.0*N_tie/N_games))
        

    def run(self,agents):
        self.agents=agents
        self.wins=[]
        for game in range(self.number_of_games):

            if self.display:
                _print("====")
                _print("Game ",game+1)
            self.state=self.initial_state()
            

            if self.save_states:
                game_dict={}
                self.games.append(game_dict)
                game_dict['states']=[deepcopy(self.state)]
                game_dict['moves']=[]
                game_dict['players']=[]


            player,other_player=1,2
            agents=[None,agent1,agent2]  # make a 1-index list

            for agent in agents[1:]:
                agent.states=[]
                agent.actions=[]
                agent.last_action=None
                agent.last_state=None
                agent.last_player=None
                arginfo=inspect.getargspec(agent.move)
                agent.move_args=len(arginfo.args)
            
            move_count=1
            while True:

                if move_count==player:
                    try:
                        agents[player].pre(self.state,agents[player])
                    except (AttributeError,KeyError):
                        pass
                        
                valid_move=False
                count=0
                auto_lose=False
                
                while not valid_move:
                    if self.display:
                        self.show_state(self.state)

                    if agents[player].move_args==3:
                        move=agents[player].move(self.state,player,agents[player])
                    else:
                        move=agents[player].move(self.state,player)
                        
                    if move =='':
                        raise ValueError("Empty move quits. ")
                        
                    if self.display:
                        _print("Player %d moves %s" % (player,str(move)))
                        
                    valid_move=self.is_valid_move(player,move)
                    if not valid_move:
                        if self.display:
                            _print("Illegal move by the agent %s: %s.  Automatic Loss." % (str(agents[player]),str(move)))

                        valid_move=True
                        auto_lose=True

                move_count+=1
                agents[player].states.append(deepcopy(self.state))
                agents[player].actions.append(deepcopy(move))
                agents[player].last_action=deepcopy(move)
                agents[player].last_state=deepcopy(self.state)
                agents[player].last_player=player

                if auto_lose:
                    status='lose'
                    break
                
                new_state=self.update_state(deepcopy(self.state),player,move)
                repeat=self.repeat_move(deepcopy(self.state),player,move)

                self.state=new_state
                if self.save_states:
                    game_dict['states'].append(deepcopy(self.state))
                    game_dict['moves'].append(deepcopy(move))
                    game_dict['players'].append(player)


                status=self.win_status(self.state,player)
                if not status in ['win','lose','stalemate',None]:
                    raise ValueError("Win status returned '%s' not valid.  Allowed values only in ['win','lose','stalemate',None]." % status)

                if status:
                    break

                if repeat:
                    continue
                
                player,other_player=other_player,player


            if self.display:
                self.show_state(self.state)
                
            stati=[None,None,None]
            if status=='win':
                if self.display:
                    _print("Player ",player,"won.")
                self.wins.append(player)

                stati[player]='win'
                stati[other_player]='lose'

            elif status=='lose':
                if self.display:
                    _print("Player ",other_player,"won.")
                self.wins.append(other_player)
                stati[player]='lose'
                stati[other_player]='win'
            else: # stalemate
                if self.display:
                    _print("Neither player won: ",status)
                self.wins.append(0)
                stati[player]='stalemate'
                stati[other_player]='stalemate'

            try:
                agent1.post(stati[1],1,agent1)
            except (AttributeError,KeyError):
                pass
                
            try:
                agent2.post(stati[2],2,agent2)
            except (AttributeError,KeyError):
                pass

        return self.wins


def argmax(v):

    y=list(zip(v,list(range(len(v)))))
    return max(y)[1]

def epsilon_greedy_choice(choices,weights=None,epsilon=0.1):

    r=random.random()
    if r<epsilon:
        return weighted_choice(choices,weights)
    else:
        return top_choice(choices,weights)
        
def random_choice(choices):
    
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
            
        return random.choice(choices)
    
    try:
        choices=list(range(len(choices.ravel())))
    except AttributeError:
        choices=list(range(len(choices)))
    
    return random.choice(choices)

def all_same(L):
  return all(x == L[0] for x in L)

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

        if all_same(weights):
            return random.choice(choices)

        i=argmax(weights)
        return choices[i]

    if weights is None:
        try:
            weights=choices.ravel()
        except AttributeError:
            weights=choices

        i=argmax(weights)
        return i
    else:
        if all_same(weights):
            return random.choice(choices)

        i=argmax(weights)
        return choices[i]

        
def weighted_choice(choices,weights=None):
    import random

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
    elif weights is None:

        try:
            weights=choices.ravel()
        except AttributeError:
            weights=choices

        choices=None

    # calculate the cumulative sum
    s=0.0
    norm_weights=[]
    for weight in weights:
        s+=weight
        norm_weights.append(s)

    total=norm_weights[-1]

    if total==0.0:  # all are bad, so return None
        return None

    norm_weights=[w/total for w in norm_weights]

    r=random.random()

    for i,w in enumerate(norm_weights):
        if r<=w:
            break

    else:
        raise ValueError("Wrong random number: "+str(r)+" for "+str(norm_weights))

    
    if isinstance(choices,dict):  # given a dictionary
        return choices[i]  
    elif choices is None:
        return i  
    else:
        return choices[i]


