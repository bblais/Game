#!/usr/bin/env python
# coding: utf-8

# https://en.wikipedia.org/wiki/Goofspiel

# Goofspiel is played using cards from a standard deck of cards, and is typically a two-player game,[4] although more players are possible. Each suit is ranked A (low), 2, ..., 10, J, Q, K (high).
# 
# One suit is singled out as the "prizes"; each of the remaining suits becomes a hand for one player, with one suit discarded if there are only two players, or taken from additional decks if there are four or more. The prizes are shuffled and placed between the players with one card turned up.
# 
# Play proceeds in a series of rounds. The players make sealed bids for the top (face up) prize by selecting a card from their hand (keeping their choice secret from their opponent). Once these cards are selected, they are simultaneously revealed, and the player making the highest bid takes the competition card. Rules for ties in the bidding vary, possibilities including the competition card being discarded, or its value split between the tied players (possibly resulting in fractional scores).[1] Some play that the current prize "rolls over" to the next round, so that two or more cards are competed for at once with a single bid card.
# 
# The cards used for bidding are discarded, and play continues with a new upturned prize card.
# 
# After 13 rounds, there are no remaining cards and the game ends. Typically, players earn points equal to sum of the ranks of cards won (i.e. ace is worth one point, 2 is two points, etc., jack 11, queen 12, and king 13 points). Players may agree upon other scoring schemes.

# In[ ]:


class CardTrickGame(object):
    """
    The moves are simultaneous
    """
    
    def __init__(self,number_of_games=1,display=True,**kwargs):
        
        self.display=display
        self.state=None
        self.params=kwargs
        
        self.simultaneous_moves=False
        
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

                if not self.simultaneous_moves:
                    if move_count==player:
                        try:
                            agents[player].pre(self.state,agents[player])
                        except (AttributeError,KeyError):
                            pass

                    valid_move=False
                    count=0
                    auto_lose=False

                    moves=[]
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

            else:  # simultaneous
                    if move_count==player:
                        try:
                            agents[player].pre(self.state,agents[player])
                        except (AttributeError,KeyError):
                            pass

                    valid_move=False
                    count=0
                    auto_lose=False

                    moves=[]
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


# In[1]:


def initial_state(N=13):  # this is the full state
    deck=[]
    for rank in range(1,N+1):
        for suit in ['h']:
            c=Card(rank,suit)
            deck.append(c)

    random.shuffle(deck)

    hands=[]
    hand=[]
    for rank in range(1,N+1):
        for suit in ['s']:
            c=Card(rank,suit)
            hand.append(c)
    hands.append(hand)
    
    hand=[]
    for rank in range(1,N+1):
        for suit in ['c']:
            c=Card(rank,suit)
            hand.append(c)
    hands.append(hand)
    
    return deck,hands


# In[2]:


def state_to_observation(state,player):
    return hands[player-1]


# In[3]:


def show_state(observation,player):
    print(state,player)


# In[4]:


def valid_moves(observation,player):
    hand=observation
    return hand


# In[ ]:


def 

