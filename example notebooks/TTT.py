
# coding: utf-8

# In[1]:

from Game import *


# In[2]:

def initial_state():
    return Board(3,3)


# In[3]:

def valid_moves(board,player):

    empty=[]
    for i in range(9):
        if board[i]==0:
            empty.append(i)

    return empty


# In[4]:

def check_three_in_a_row(row):

    if row[0]==1 and row[1]==1 and row[2]==1:
        return 1
    elif row[0]==2 and row[1]==2 and row[2]==2:
        return 2
    else:
        return 0


# In[5]:

def win_status(board,player):
    # in ttt, after a move, that player can either win or stalemate
    # they can't lose after their own move
    
    if check_three_in_a_row( [board[0],board[1],board[2] ])==player:
        return 'win'

    if check_three_in_a_row( [board[2],board[5],board[8] ])==player:
        return 'win'

    if check_three_in_a_row( [board[3],board[4],board[5] ])==player:
        return 'win'

    if check_three_in_a_row( [board[6],board[7],board[8] ])==player:
        return 'win'

    if check_three_in_a_row( [board[0],board[3],board[6] ])==player:
        return 'win'

    if check_three_in_a_row( [board[1],board[4],board[7] ])==player:
        return 'win'

    if check_three_in_a_row( [board[0],board[4],board[8] ])==player:
        return 'win'

    if check_three_in_a_row( [board[6],board[4],board[2] ])==player:
        return 'win'


    # stalemate
    tie=True
    for i in range(9):
        if board[i]==0:
            tie=False

    if tie:
        return 'stalemate'



    return None


# In[6]:

def update_state(board,player,move):
    board[move]=player
    return board


# In[7]:

def print_row(row):

    line=''
    if row[0]==0:
        line=line+'   '
    elif row[0]==1:
        line=line+' X '
    else:
        line=line+' O '

    line=line+'|'

    if row[1]==0:
        line=line+'   '
    elif row[1]==1:
        line=line+' X '
    else:
        line=line+' O '

    line=line+'|'

    if row[2]==0:
        line=line+'   '
    elif row[2]==1:
        line=line+' X '
    else:
        line=line+' O '

    line=line+'|'
    print(line)


# In[8]:

def show_state(board):

    print_row( [ board[0],board[1],board[2] ])
    print("---+---+---")
    print_row( [ board[3],board[4],board[5] ])
    print("---+---+---")
    print_row( [ board[6],board[7],board[8]])
    
    print()
    print("Choices:")
    print("""
     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8
    """)


# In[9]:

def random_move(state,player):

    moves=valid_moves(state,player)
    return random.choice(moves)

def human_move(state,player):
    print("Player ", player, end=' ')
    valid_move=False
    while not valid_move:
        move=eval(input('What is your move? '))

        if move in valid_moves(state,player):
            valid_move=True
        else:
            print("Illegal move.")

    return move
 


# In[10]:

human_agent=Agent(human_move)
random_agent=Agent(random_move)


g=Game(number_of_games=1)
g.run(human_agent,random_agent)
g.report()   # state the percentage of wins, ties, etc...


# In[ ]:



