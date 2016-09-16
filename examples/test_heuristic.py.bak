from Game import *

def heuristic(state,player):

    B=state
    
    total=0.0
    count=0
    for row in B.rows(3):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.95
            else:
                total-=0.95
        count+=3
    for row in B.rows(2):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.5
            else:
                total-=0.5
        count+=2
    for row in B.cols(3):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.95
            else:
                total-=0.95
        count+=3
    for row in B.cols(2):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.5
            else:
                total-=0.5
        count+=2
    for row in B.diags(3):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.95
            else:
                total-=0.95
        count+=3
    for row in B.diags(2):
        for value in row:
            if value==0:
                total+=0.0
            elif value==player:
                total+=0.5
            else:
                total-=0.5
        count+=2
        
    total=total/count

    return (total+1)/2
    
B=Board(5,6)

for i in range(30):
    if random.random()<0.75:
        B[i]=random.randint(0,2)
    else:
        B[i]=0
        
print B

print heuristic(B,1)
print heuristic(B,2)

