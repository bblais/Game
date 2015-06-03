# README #

This is a Game simulator, written in Python, for making simple board and card games.

## Definitions

### These functions need to be named exactly this:

    def initial_state(): 
    """ returns  - The initial state of the game"""
    
    def valid_moves(state,player):
    """returns  - a list of the valid moves for the state and player"""

    def show_state(state):
    """prints or shows the current state"""

    def update_state(state,player,move):
    """returns  - the new state after the move for the player"""

    def win_status(state,player):
    """    returns  - 'win'  if the state is a winning state for the player, 
               'lose' if the state is a losing state for the player,
               'stalemate' for a stalemate
               None otherwise
    """


### This function is optional:

    def repeat_move(state,player,move):
    """
    returns  - True, if the current player gets another move right 
               after this one.  returns False otherwise.
    """

### This function can be named something else:

    def my_agent_move(state,player):  # optional third-arg info
    """  returns - a valid move """
   
## Usage

    def random_move(state,player):    
        moves=valid_moves(state,player)
        return random.choice(moves)
    
    random_agent=Agent(random_move)

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
