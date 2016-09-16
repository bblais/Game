from Game import *

def initial_state():
    b=Board(3,3)
    b.pieces=['.','X','O']
    return b
    
def valid_moves(state,player):
    return state.find(0)

def win_status(state,player):
    # in ttt, after a move, that player can either win or stalemate
    # they can't lose after their own move
    
    for row in state.rows():
        if row==[player,player,player]:
            return 'win'

    for col in state.cols():
        if col==[player,player,player]:
            return 'win'
    
    for diag in state.diags():
        if diag==[player,player,player]:
            return 'win'
    
    if not state.find(0):
        return 'stalemate'
        
    return None

def update_state(board,player,move):
    board[move]=player
    return board


def show_state(board):
    print board
    
    print
    print "Choices:"
    print """
     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8
    """

def random_move(state,player):

    moves=valid_moves(state,player)
    return random.choice(moves)

def human_move(state,player):
    print "Player ", player,
    valid_move=False
    while not valid_move:
        move=input('What is your move? ')

        if move in valid_moves(state,player):
            valid_move=True
        else:
            print "Illegal move."

    return move
    
  
human_agent=Agent(human_move)
random_agent=Agent(random_move)


g=Game(number_of_games=1)
g.run(human_agent,random_agent)
g.report()   # state the percentage of wins, ties, etc...







