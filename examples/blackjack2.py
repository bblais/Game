from __future__ import division
from Game import *
from Struct import *

def initial_state(agents,number_of_decks=1):
    deck=makedeck(number_of_decks,shuffle=True)

    hands=[]
    # deal two for every agent
    for agent in agents:
        agent.hand=deal(deck,2)
        hands.append(agent.hand)
    
    return deck,hands



def value(hand):
    has_ace=False
    val=0
    for card in hand:
        if card.rank==1:
            has_ace=True
            
        if card.rank>10:
            val+=10
        else:
            val+=card.rank
        
    if has_ace and val+10<21:
        val+=10
        
    return val



def play(agents,number_of_decks=1,
        number_of_games=1,display=True):

    all_scores=[]

    for agent in agents:
        agent.score=0

    for game in range(number_of_games):    
    
        deck=makedeck(number_of_decks,shuffle=True)
        hands=[]
        # deal two for every agent
        for agent in agents:
            agent.hand=deal(deck,2)
            hands.append(agent.hand)
            
        for agent in agents:
            # shown is all of the cards for all agents, 
            # except the first card
            shown={}
            for agent2 in agents:
                shown[agent2.name]=agent2.hand[1:]

            hand=agent.hand
            
            if display:
                print agent.name,"'s move"
                print "\tShown is ",shown
                print "\tYour hand is:",hand
                
            while True:  # keep going until stay or bust
                move=agent.move(hand,shown,agent)
                if display:
                    print "\t Move: ",move
                if move=='s':
                    break
                agent.hand.extend(deal(deck))

                if display:
                    print agent.name
                    print "\tShown is ",shown
                    print "\tYour hand is:",hand

                if value(agent.hand)>21:
                    if display:
                        print "\tBust!"
                    break

        if display:
            print "Results"
            for agent in agents:
                print agent.name
                print "\t",agent.hand
                print "\t",value(agent.hand)
                if value(agent.hand)>21:
                    print "\t\tBust!"
                    
                
        winners=[]
        max_so_far=-1
        for agent in agents:
            score=value(agent.hand)
            if score>21:  # busting doesn't win
                continue
            if score>max_so_far:
                winners=[agent]
                max_so_far=score
            elif score==max_so_far:
                winners.append(agent)
                max_so_far=score
            else:
                pass
                
        # dealer wins in a tie
        if dealer_agent in winners:
            winners=[dealer_agent]

        if display:
            print "Winners:"
            for agent in winners:
                print "\t",agent.name
                
        for agent in winners:
            agent.score+=1

        if display:
            print "================="
          
    return [agent.score for agent in agents]
    
def dealer_move(hand,shown,info=None):

    val=value(hand)
    if val<=16:
        return 'h'
    else:
        return 's'


def human_move(hand,shown,info=None):
    move=raw_input('Hit or stay? ')    
    move=move.lower()[0]
    return move    
    
def random_move(hand,shown,info=None):
    return random.choice(['h','s'])
    

human_agent=Agent(human_move)
human_agent.name='Human'

dealer_agent=Agent(dealer_move)
dealer_agent.name='Dealer'

random_agent=Agent(random_move)
random_agent.name='Bob'
    

   
agents=[human_agent,random_agent,dealer_agent]

# g=CardGame(number_of_games=1)
# g.run(agents,number_of_decks=1)
# g.report()

self=Struct()
self.agents=agents
self.number_of_games=1
self.initial_state=initial_state
self.save_states=False
self.games=[]



if __name__=="__main__":

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

                try:
                    move=agents[player].move(self.state,player,agents[player])
                except TypeError:
                    move=agents[player].move(self.state,player)
                    
                if move =='':
                    raise ValueError,"Empty move quits. "
                    
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

