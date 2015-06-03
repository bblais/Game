from Game import *

def initial_state():
    b=Board(8,8)
    b.pieces=['.','x','o']
    
    b[1]=1  # fox
    row=7
    for col in [1,3,5,7]:
        b[row,col-1]=2

            
    return b
    
def show_state(state):
    # A clever way to print the board
    tempboard=Board(8,8)
    tempboard.board=range(8*8)
    tempboard.pieces=[str(i) for i in range(8*8)]
    tempboard.pieces.extend(['x','o'])  # 64=x, 65=o
    
    for x in state.find(1):
        tempboard[x]=64
    for x in state.find(2):
        tempboard[x]=65
    
    print tempboard

    #print state
    
    
def get_human_move(state,player):
    print "Player ",player
        
    if player==1: # there is only one fox, so find it:
        start=state.find(1)[0]
        print "Starting position for move?",start
    else:
        start=input("Starting position for move?")
        
    end=input("Ending position for move?")
    
    move=[start,end]
    
    return move
    
def win_status(state,player):
    if player==1: # fox wins by reaching last row
        position=state.find(1)[0]
        if position>=56:
            return 'win'
            
    if player==2:  # hounds win by trapping fox
        if not valid_moves(state,1):
            return 'win'
            
def update_state(state,player,move):
    newstate=state
    p1,p2=move
    newstate[p1]=0
    newstate[p2]=player
    return newstate
    
def valid_moves(state,player):
    all_moves=[]
    if player==1: # fox can move diagonally in any direction not 
        for move in state.diag_positions(2): # every length-2 diagonal on the board
            p1,p2=move
            if state[p1]==1 and state[p2]==0:
                all_moves.append([p1,p2])
            if state[p2]==1 and state[p1]==0:
                all_moves.append([p2,p1])
    else:  # hounds can only move forward, which means smaller position                        
        for move in state.diag_positions(2): # every length-2 diagonal on the board
            p1,p2=move
            if p1<p2:
                p1,p2=p2,p1  # swap if bigger, so we know that p1 is smaller than p2
            if state[p1]==2 and state[p2]==0:
                all_moves.append([p1,p2])

    return all_moves
    
def random_move(state,player):    
    moves=valid_moves(state,player)
    return random.choice(moves)
    
random_agent=Agent(random_move)
my_agent=Agent(get_human_move)
    
g=Game(number_of_games=1)
g.run(random_agent,my_agent)
g.report()    
