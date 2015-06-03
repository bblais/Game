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
        return 'Win'
    
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


human_agent=Agent(human_move)
random_agent=Agent(random_move)


g=Game(number_of_games=1)
g.run(random_agent,random_agent)
g.report()









