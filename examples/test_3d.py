from Game import *

b=Board(3,3,3)


# these aren't normal piece values, but it is useful
# to see the choices
for i in range(len(b)):
    b[i]=i
    
print b

print "Rows:"
for row in b.rows():
    print row

print "Cols:"
for col in b.cols():
    print col


# not sure what a good name for this is...
# is there a better name?
print "Heights:"  
for col in b.heights():
    print col
    
print "Diags:"
for diag in b.diags():
    print diag
    
    
    
# so a ttt win status could look like:

def win_status(state,player):

    for row in b.rows():
        if row==[player,player,player]:
            return 'win'
            
    for col in b.cols():
        if col==[player,player,player]:
            return 'win'
            
    for diag in b.diags():
        if diag==[player,player,player]:
            return 'win'
    
    
    
# want to print pieces?  try this:

# blank board
b=Board(3,3,3)
b.pieces=['.','X','O']

# put some random pieces down
b[4]=1
b[7]=1
b[21]=2
b[14]=1
b[2]=2
b[11]=2

print b

# want to count the fraction of 2 in a row?

player=1
total=0
two_in_a_row=0

for col in b.cols():
    if col.count(player)==2:
        two_in_a_row+=1
    total+=1
for row in b.rows():
    if row.count(player)==2:
        two_in_a_row+=1
    total+=1
    
# etc... with heights and diags....

print "Player",player,"has ",two_in_a_row," twos in a row out of",total



# want to find the two in a row?
