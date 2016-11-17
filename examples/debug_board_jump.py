from board import *

b=Board(4,4)
b[3,1]=1
b[3,2]=1
b[1,1]=1
b[1,2]=1
b[2,1]=2
b[2,2]=2

print(b)
b.show_locations()
print(b.moves(1,'jn'))

print("==")

print(b.moves(1,'jnw'))

print("==")

print(b.moves(1,'jse'))