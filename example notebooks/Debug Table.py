#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Game import *


# In[2]:


Q=LoadTable('/Users/bblais/Desktop/ai373/AI-and-Robotics-Fall-2019-Class-Notebooks/TTT Skittles 2.json')


# In[3]:


board=list(Q.keys())[0]


# In[4]:


board


# In[5]:


T=Table()
B=Board(3,3)
B[1]=1
B[3]=2


# In[6]:


B.__hash__()


# In[7]:


B


# In[8]:


B.board


# In[9]:


def board2int(B):
    N=9  # first digit
    for v in B.board:
        N=N*10+v
        
    return N
    
    


# In[10]:


board2int(B)


# In[11]:


int(B)


# In[ ]:




