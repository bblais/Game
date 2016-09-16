from __future__ import division
from Game import *

def value(hand):
    has_ace=False
    val=0
    for card in hand:
        if card.rank==1:
            has_ace=True
        val+=card.rank

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

        for agent in agents:
            try:
                if agent in winners:
                    agent.post('win',agent)
                else:
                    agent.post('lose',agent)
            except (AttributeError,KeyError):
                pass


        if display:
            print "================="
          
    return [agent.score for agent in agents]
    
def dealer_move(hand,shown,info=None):

    val=value(hand)
    if val<16:
        return 'h'
    else:
        return 's'

def dealer_move2(hand,shown,info=None):

    val=value(hand)
    if val<16:
        return 'h'
    else:
        return 's'
    
    

def human_move(hand,shown,info=None):
    move=raw_input('Hit or stay? ')    
    move=move.lower()[0]
    return move    
    
def random_move(hand,shown,info=None):
    return random.choice(['h','s'])
    
    
    
def get_state(hand,shown):
    state=value(hand)
    
    has_ace=False
    for card in hand:
        if card.rank==1:
            has_ace=True
            
    if has_ace:
        state+=100
        
    return state

def Q_BJ_move(hand,shown,info):
    Q=info.Q
    last_action=info.last_action
    last_state=info.last_state
    alpha=info.alpha
    gamma=info.gamma
    epsilon=info.epsilon

    state=get_state(hand,shown)

    if not state in Q:
        Q[state]=Table()
        for action in ['h','s']:
            Q[state][action]=0.0

    if random.random()<epsilon: # random move
        action=random_choice(Q[state])
    else:
        action=top_choice(Q[state])

    if not last_action is None:
        r=0.0
        Q[last_state][last_action]+=alpha*(r+
                gamma*max([Q[state][a] for a in Q[state]])-
                Q[last_state][last_action])

    info.last_action=action
    info.last_state=state
    
    return action

def Q_BJ_after(status,info):
    Q=info.Q
    last_action=info.last_action
    last_state=info.last_state
    alpha=info.alpha
    gamma=info.gamma

    if status=='lose':
        r=-1.0
    elif status=='win':
        r=1.0
    else:
        r=0.0

    if not last_action is None:
        Q[last_state][last_action]+=alpha*(r-
                Q[last_state][last_action])

    info.last_action=None
    info.last_state=None
    
    
learning_agent=Agent(Q_BJ_move)
learning_agent.post=Q_BJ_after
learning_agent.name='Smarty'
learning_agent.Q=Remember()
learning_agent.last_action=None
learning_agent.last_state=None


human_agent=Agent(human_move)
human_agent.name='Human'

dealer_agent=Agent(dealer_move)
dealer_agent.name='Dealer'

dealy_agent=Agent(dealer_move2)
dealy_agent.name='Dealy'

random_agent=Agent(random_move)
random_agent.name='Bob'
   
agents=[learning_agent,dealer_agent]

for i in range(10):

    learning_agent.alpha=0.3  # learning rate
    learning_agent.gamma=0.9  # memory
    learning_agent.epsilon=0.1  # chance of making random move
    scores=play(agents,
                number_of_games=5,
                display=False)
                
    Remember(learning_agent.Q)

    learning_agent.alpha=0.0  # learning rate
    learning_agent.gamma=0.9  # memory
    learning_agent.epsilon=0  # chance of making random move
    scores=play(agents,
                number_of_games=100,
                display=False)

    print scores
