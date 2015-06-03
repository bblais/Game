from Game import *

def initial_state():

    return 18


def valid_moves(state,player):

    if state==1:
        return [1]
    elif state==2:
        return [1,2]
    else:
        return [1,2,3]
        

def show_state(state):

    print "There are ",state," sticks left."


def update_state(state,player,move):

    new_state=state-move
    return new_state


def win_status(state,player):


    if state==1:
        return 'win'
    
    elif state==0:
        return 'lose'
    
    else:
        return None



# agents

def random_move(state,player):
    
    moves=valid_moves(state,player)
    return random.choice(moves)

def human_move(state,player):

    move=input('Take 1, 2 or 3 sticks ')
    return move

def table_move(state,player,info):
    T=info.T
    return T[state]


human_agent=Agent(human_move)
random_agent=Agent(random_move)
table_agent=Agent(table_move)
table_agent.T=Table()
T=table_agent.T

T[1]=1
T[2]=1
T[3]=2
T[4]=3
T[5]=1
T[6]=1
T[7]=2
T[8]=3
T[9]=1
T[10]=1
T[11]=2
T[12]=3
T[13]=1
T[14]=1
T[15]=2
T[16]=3
T[17]=1
T[18]=1
T[19]=2
T[20]=3



g=Game(number_of_games=1)
g.run(human_agent,table_agent)
g.report()









