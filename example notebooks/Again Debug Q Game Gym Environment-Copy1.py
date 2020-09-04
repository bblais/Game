#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *


# In[2]:


def initial_state():
    b=Board(3,3)
    b.pieces=['.','X','O']
    return b


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


def show_state(board):

    print(board)
    
    print()
    print("Choices:")
    print("""
     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8
    """)


# In[ ]:





# In[8]:


def random_move(state,player,memory=None):

    moves=valid_moves(state,player)
    return random.choice(moves)

def first_move(state,player,memory=None):

    moves=valid_moves(state,player)
    return moves[0]

def human_move(state,player,memory=None):
    print("Player ", player, end=' ')
    valid_move=False
    while not valid_move:
        move=eval(input('What is your move? '))

        if move in valid_moves(state,player):
            valid_move=True
        else:
            print("Illegal move.")

    return move
 


# In[9]:


human_agent=Agent(human_move)
random_agent=Agent(random_move)
first_agent=Agent(first_move)


# In[10]:


# g=Game(number_of_games=1)
# g.run(human_agent,random_agent)
# g.report()   # state the percentage of wins, ties, etc...


# In[11]:


from collections import UserList
class ActionList(UserList):
    
    def sample(self):
        return random.choice(self)

from copy import deepcopy
class GameEnv(object):
    
    def __init__(self,**kwargs):
        self.functions=Struct()
        
        if not 'initial_state' in kwargs:
            self.functions.initial_state=initial_state
            self.functions.valid_moves=valid_moves
            self.functions.update_state=update_state
            self.functions.show_state=show_state
            self.functions.win_status=win_status
        else:
            self.functions.initial_state=kwargs['initial_state']
            self.functions.valid_moves=kwargs['valid_moves']
            self.functions.update_state=kwargs['update_state']
            self.functions.show_state=kwargs['show_state']
            self.functions.win_status=kwargs['win_status']
            

        self.reset()
    
    def reset(self):
        self.player=1
        self.state=self.functions.initial_state(),self.player
    
        observation=self.state
        return observation

    def render(self,mode='human'):
        if mode=='human':
            board,player=self.state
        
            print(f"Player {player}\nBoard:\n{board}")
        else:
            raise NotImplementedError
    
    @property
    def action_space(self):
        board,player=self.state
        valid_moves=self.functions.valid_moves(board,player)
        return ActionList(valid_moves)
    
    def step(self,action):
        board,player=self.state
        valid_moves=self.functions.valid_moves(board,player)

        if action not in valid_moves:
            observation,reward,done,info=self.state,-1000,True,None
            return observation,reward,done,info
        
        
        move=action
        board=deepcopy(board)  # update state might change the board
        new_board=self.functions.update_state(board,player,move)
        
        status=self.functions.win_status(new_board,player)
        if status=='win':
            observation,reward,done,info=self.state,100,True,None
            return observation,reward,done,info
        elif status=='lose':
            observation,reward,done,info=self.state,-100,True,None
            return observation,reward,done,info
        elif status=='stalemate':
            observation,reward,done,info=self.state,0,True,None
            return observation,reward,done,info
        elif status is None:
            if self.player==1:
                self.player=2
            else:
                self.player=1
                
            self.state=new_board,self.player

            observation,reward,done,info=self.state,0,False,None
            return observation,reward,done,info
        else:
            raise ValueError
    
    def close(self):
        pass
    
    


# ## Can I do Q-learning?

# In[12]:


def Q_move(board,player,memory):  # just the move
    Q=memory.Q
    alpha=memory.alpha
    gamma=memory.gamma
    epsilon=memory.epsilon
    
    if not board in Q:
        Q[board]=Table()
        for action in valid_moves(board,player):
            Q[board][action]=0.0

    if random.random()<epsilon:  # random move
        action=random_choice(Q[board])
    else:
        action=top_choice(Q[board])

    return action

        
    
def Q_update(observation,action,reward,done,memory):
    Q=memory.Q
    alpha=memory.alpha
    gamma=memory.gamma
    epsilon=memory.epsilon
    
    last_action=memory.last_action
    
    if last_action is None:  # first move
        memory.last_observation=observation
        memory.last_action=action        
        return

    last_observation = memory.last_observation
    
    if done:
        last_board,player = last_observation
        Q[last_board][last_action]+=alpha*(reward - Q[last_board][last_action] )
    else:
        last_board,player = last_observation
        new_board,new_player = observation
        assert player==new_player
    
        Q[last_board][last_action]+=alpha*(reward + 
                                 gamma*max([Q[new_board][a] for a in Q[new_board]]) - 
                                 Q[last_board][last_action] )  
        
        
    memory.last_observation=observation
    memory.last_action=action
        


# In[13]:


from numpy import exp


# In[61]:


Qmemory=Struct()
Qmemory.Q=Table()
Qmemory.alpha=0.3
Qmemory.gamma=0.9

min_epsilon=0.01
max_epsilon=0.5
Qmemory.epsilon=max_epsilon
Qmemory.epsilon_decay=0.01      

Q_agent=Agent(Q_move,update=Q_update,memory=Qmemory)


# In[62]:


train_episodes = 1000    
test_every=10
test_episodes = 200
max_steps=500


# In[63]:


agents={1:Q_agent,
        2:first_agent,
       }

env = GameEnv(initial_state=initial_state,
             update_state=update_state,
             show_state=show_state,
             win_status=win_status,
             valid_moves=valid_moves)

#Training the agent

#Creating lists to keep track of reward and epsilon values
training_rewards = []
epsilons = []
fraction_wins=[]
fraction_losses=[]
fraction_ties=[]

for episode in range(train_episodes):
    #Reseting the environment each time as per requirement
    observation = env.reset()

    for key in agents:
        agents[key].memory.last_action=None
    
    #Starting the tracker for the rewards
    total_training_rewards = 0
    
    for step in range(max_steps):
        #env.render()
        
        board,player=observation
        other_player=3-player
        
        memory=agents[player].memory
        action=agents[player].move(board,player,memory)
        #print(f"action: {action}")
        new_observation, reward, done, info = env.step(action)
        
        if not done:
            assert reward==0
            
        agents[player].update(observation,action,reward,done,memory)
        
        
        if done:
            #update again with the recently won/lost move
            agents[player].update(observation,action,reward,done,memory)
            
            memory=agents[other_player].memory
            agents[other_player].update(observation,action,-reward,done,memory)
            
            if player==1:
                total_training_rewards += reward      
            else:
                total_training_rewards += -reward      
            
            
        observation = new_observation     
        
        #Ending the episode
        if done == True:
            #print ("Total reward for episode {}: {}".format(episode, total_training_rewards))
            break
    
    #Cutting down on exploration by reducing the epsilon 
    memory=agents[1].memory
    epsilon=memory.epsilon
    decay_epsilon=memory.epsilon_decay
    memory.epsilon = min_epsilon + (max_epsilon - min_epsilon)*exp(-decay_epsilon*episode)
    
    #Adding the total reward and reduced epsilon values
    training_rewards.append(total_training_rewards)
    epsilons.append(epsilon)
    

    if (episode+1) % test_every ==0:
        wins=0
        losses=0
        ties=0

        for test_episode in range(test_episodes):
            observation = env.reset()

            for key in agents:
                agents[key].last_action=None

            for step in range(max_steps):
                #env.render()

                board,player=observation
                other_player=3-player


                memory=agents[player].memory
                action=agents[player].move(board,player,memory)
                #print(f"action: {action}")
                new_observation, reward, done, info = env.step(action)

                observation = new_observation   


                if done:
                    if player==2:
                        reward=-reward

                    if reward==100:
                        wins+=1
                    elif reward==-100:
                        losses+=1
                    elif reward==0:
                        ties+=1
                    else:
                        raise ValueError


                    break

        fraction_wins.append(wins/test_episodes*100)
        fraction_losses.append(losses/test_episodes*100)
        fraction_ties.append(ties/test_episodes*100)
    
        #print(fraction_wins[-1],fraction_losses[-1],fraction_ties[-1])
    
print ("Training score over time: " + str(sum(training_rewards)/train_episodes))


            
        


# In[64]:


get_ipython().run_line_magic('pylab', 'inline')


# In[65]:


#Visualizing results and total reward over all episodes
x = range(train_episodes)
plot(x, training_rewards)
xlabel('Episode')
ylabel('Training total reward')
title('Total rewards over all episodes in training') 
show()


# In[66]:


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)


# In[67]:


N=10
plot(x[N-1:], running_mean(training_rewards,N))


# In[68]:


plot(epsilons)


# In[69]:


plot(fraction_wins)


# In[59]:


wins


# In[ ]:




