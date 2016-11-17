def prod(A):
    p=1
    for val in A:
        p*=val
    return p

class Board(object):

    def __init__(self,*args):
        self.shape=args
        self.dimension=len(self.shape)
        self.board=[0]*prod(args)
        self.pieces=None
        
    def immutable(self):
        return tuple(self.board)
        
    def __len__(self):
        return len(self.board)
        
    def find(self,player):
        locations=[]
        for i in range(len(self)):
            if self.board[i]==player:
                locations.append(i)
        return locations
        
    def index_from_rc(self,rc,c=None):
        if not c is None:
            rc=[rc,c]
        if isinstance(rc,int):
            index=rc
            if rc>=len(self.board) or rc<0:
                raise IndexError("Illegal index")
        elif len(self.shape)==1:
            index=rc[0]
            if index>=length(self.board) or rc<0:
                raise IndexError("Illegal index")
        elif len(self.shape)==2:
            r,c=rc
            
            if r>=self.shape[0] or r<0:
                raise IndexError("Illegal row")
            if c>=self.shape[1] or c<0:
                raise IndexError("Illegal col")
                
            index=r*self.shape[1]+c
        elif len(self.shape)==3:
            r,c,h=rc
            if r>=self.shape[0] or r<0:
                raise IndexError("Illegal row")
            if c>=self.shape[1] or c<0:
                raise IndexError("Illegal col")
            if h>=self.shape[2] or h<0:
                raise IndexError("Illegal height")
            
            index=h*self.shape[0]*self.shape[1]+r*self.shape[1]+c
            
        else:
            raise ValueError("Not implemented")
            
        return index
        
    def rc_from_index(self,index):
        if isinstance(index,list):
            rc=[rc_from_index(i) for i in index]
            return rc
            
        if len(self.shape)==1:
            rc=index
            assert index<length(self.board)
            return rc
            
        if len(self.shape)==2:
            num_rows,num_cols=self.shape
            r=index//num_cols
            c=index%num_cols
            return (r,c)
            
        if len(self.shape)==3:
            num_rows,num_cols,num_h=self.shape
            h=index//num_cols//num_rows
            r=index//num_cols
            c=index%num_cols
            return (r,c)
        
        raise ValueError("Not implemented")  
        
        
    def __getitem__(self,key):
        index=self.index_from_rc(key)
        return self.board[index]
    def __setitem__(self,key,val):
        index=self.index_from_rc(key)
        self.board[index]=val
            
    def row_positions(self,length=None):
        
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for row in tempboard.rows(length):
            yield row

    def _get_moves(self,player,m):
        
        if 'x' in m:
            capture=True
            m=m.replace('x','')
        else:
            capture=False

        if 'j' in m:
            jump=True
            m=m.replace('j','')
        else:
            jump=False      

        all_moves=[]

        if jump:
            if m=='n':
                for col in self.col_positions(3):
                    p1,pm,p2=col  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p2]==player and self[p1]==0 and 
                        self[pm]!=0 and self[pm]!=player):
                            all_moves.append( [p2,p1] )

            if m=='s':
                for col in self.col_positions(3):
                    p1,pm,p2=col  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                        self[pm]!=0 and self[pm]!=player):
                            all_moves.append( [p1,p2] )
            
            if m=='e':
                for row in self.row_positions(3):
                    p1,pm,p2=row  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                        self[pm]!=0 and self[pm]!=player):
                            all_moves.append( [p1,p2] )

            if m=='w':
                for row in self.col_positions(3):
                    p1,pm,p2=row  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p2]==player and self[p1]==0 and 
                        self[pm]!=0 and self[pm]!=player):
                            all_moves.append( [p2,p1] )

            if m=='ne':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p2]==player and self[p1]==0 and 
                            p2-p1==2*self.shape[1]-2 and
                            self[pm]!=0 and self[pm]!=player):
                        all_moves.append( [p2,p1] )

            if m=='nw':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1
                    
                    if (self[p2]==player and self[p1]==0 and 
                            p2-p1==2*self.shape[1]+2 and
                            self[pm]!=0 and self[pm]!=player):
                        all_moves.append( [p2,p1] )

            if m=='se':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                            p2-p1==2*self.shape[1]+2 and
                            self[pm]!=0 and self[pm]!=player):
                        all_moves.append( [p1,p2] )

            if m=='se':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                            p2-p1==2*self.shape[1]-2 and
                            self[pm]!=0 and self[pm]!=player):
                        all_moves.append( [p1,p2] )

            return all_moves


        # no jump
        if m=='n':
            for col in self.col_positions(2):
                p1,p2=col  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p2]==player and self[p1]!=0 and self[p1]!=player:
                        all_moves.append( [p2,p1] )
                else:
                    if self[p2]==player and self[p1]==0:
                        all_moves.append( [p2,p1] )

        if m=='s':
            for col in self.col_positions(2):
                p1,p2=col  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p1]==player and self[p2]!=0 and self[p2]!=player:
                        all_moves.append( [p1,p2] )
                else:
                    if self[p1]==player and self[p2]==0:
                        all_moves.append( [p1,p2] )

        if m=='e':
            for row in self.row_positions(2):
                p1,p2=row  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p1]==player and self[p2]!=0 and self[p2]!=player:
                        all_moves.append( [p1,p2] )
                else:
                    if self[p1]==player and self[p2]==0:
                        all_moves.append( [p1,p2] )
                
        if m=='w':
            for row in self.row_positions(2):
                p1,p2=row  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p2]==player and self[p1]!=0 and self[p1]!=player:
                        all_moves.append( [p2,p1] )
                else:
                    if self[p2]==player and self[p1]==0:
                        all_moves.append( [p2,p1] )

        if m=='ne':
            for diag in self.diag_positions(2):
                p1,p2=diag  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p2]==player and self[p1]!=0 and self[p1]!=player and p2-p1==self.shape[1]-1:
                        all_moves.append( [p2,p1] )
                else:
                    if self[p2]==player and self[p1]==0 and p2-p1==self.shape[1]-1:
                        all_moves.append( [p2,p1] )
             
        if m=='nw':
            for diag in self.diag_positions(2):
                p1,p2=diag  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p2]==player  and self[p1]!=0 and self[p1]!=player and p2-p1==self.shape[1]+1:
                        all_moves.append( [p2,p1] )
                else:                
                    if self[p2]==player and self[p1]==0 and p2-p1==self.shape[1]+1:
                        all_moves.append( [p2,p1] )

        if m=='se':
            for diag in self.diag_positions(2):
                p1,p2=diag  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p1]==player and self[p2]!=0 and self[p2]!=player and p2-p1==self.shape[1]+1:
                        all_moves.append( [p1,p2] )
                else:
                    if self[p1]==player and self[p2]==0 and p2-p1==self.shape[1]+1:
                        all_moves.append( [p1,p2] )
                    
        if m=='sw':
            for diag in self.diag_positions(2):
                p1,p2=diag  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if self[p1]==player  and self[p2]!=0 and self[p2]!=player and p2-p1==self.shape[1]-1:
                        all_moves.append( [p1,p2] )
                else:                    
                    if self[p1]==player and self[p2]==0 and p2-p1==self.shape[1]-1:
                        all_moves.append( [p1,p2] )
                    
        return all_moves
            
    def moves(self,player,*args):
        all_moves=[]
        for move_string in args:
            m=move_string.split(',')
            for move in m:
                move=move.lower().strip()
                all_moves.extend(self._get_moves(player,move))
        return all_moves

    def col_positions(self,length=None):
        
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for col in tempboard.cols(length):
            yield col
        
    def diag_positions(self,length=None):
        
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for diag in tempboard.diags(length):
            yield diag
            
    def __hash__(self):
        return hash(tuple(self.board))
        
    def rows(self,length=None):
        if self.dimension==1:
            for r in range(len(self.board)):
                d=[]
                keep=True
                for l in range(length):
                    try:
                        d.append(self[r+l])
                    except IndexError:
                        keep=False
                        break
                if keep:
                    yield d
                
            yield self.board
        elif self.dimension==2:
            if length==None:
                length=self.shape[1]
                
            for r in range(self.shape[0]):
                for c in range(self.shape[1]):
                    d=[]
                    keep=True
                    for l in range(length):
                        try:
                            d.append(self[r,(c+l)])
                        except IndexError:
                            keep=False
                            break
                    if keep:
                        yield d
        elif self.dimension==3:
            if length==None:
                length=self.shape[1]
                
            for h in range(self.shape[2]):
                for r in range(self.shape[0]):
                    for c in range(self.shape[1]):
                        d=[]
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[r,(c+l),h])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
        else:
            raise ValueError("not implemented for dims 4+")
            
    def heights(self,length=None):
        assert self.dimension==3

        if length==None:
            length=self.shape[2]
            
        for h in range(self.shape[2]):
            for r in range(self.shape[0]):
                for c in range(self.shape[1]):
                    d=[]
                    keep=True
                    for l in range(length):
                        try:
                            d.append(self[r,c,(h+l)])
                        except IndexError:
                            keep=False
                            break
                    if keep:
                        yield d
                
        
            
    def cols(self,length=None):
        if self.dimension==1:
            if length is None or length==1:
                for b in self.board:
                    yield b
            else:
                raise ValueError("Invalid length")
        elif self.dimension==2:
            if length==None:
                length=self.shape[1]
                
            for r in range(self.shape[0]):
                for c in range(self.shape[1]):
                    d=[]
                    keep=True
                    for l in range(length):
                        try:
                            d.append(self[(r+l),c])
                        except IndexError:
                            keep=False
                            break
                    if keep:
                        yield d
        elif self.dimension==3:
            if length==None:
                length=self.shape[1]
                
            for h in range(self.shape[2]):
                for r in range(self.shape[0]):
                    for c in range(self.shape[1]):
                        d=[]
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[(r+l),c,h])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
        else:
            raise ValueError("not implemented for dims 4+")
    
    def diags(self,length=None):
        if self.dimension==1:
            raise ValueError("No diagonals on 1D boards")
        
        if self.shape[0]!=self.shape[1] and length is None:
            raise ValueError("Need a specified diagonal length for non-square boards")
        elif length==None:
            length=self.shape[0]
        
        if self.dimension==2:
        
            for r in range(self.shape[0]):
                for c in range(self.shape[1]):
                    d=[]
                    # do right-hand diagonal
                    keep=True
                    for l in range(length):
                        try:
                            d.append(self[(r+l),(c+l)])
                        except IndexError:
                            keep=False
                            break
                    if keep:
                        yield d
        
                    d=[]
                    # do left-hand diagonal
                    keep=True
                    for l in range(length):
                        try:
                            d.append(self[(r+l),(c-l)])
                        except IndexError:
                            keep=False
                            break
                    if keep:
                        yield d

        elif self.dimension==3:
                
            for h in range(self.shape[2]):
                for r in range(self.shape[0]):
                    for c in range(self.shape[1]):
                        d=[]
                        # do right-hand diagonal
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[(r+l),(c+l),h])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
            
                        d=[]
                        # do left-hand diagonal
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[(r+l),(c-l),h])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
            
                        d=[]
                        # do right-hand diagonal, down height
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[r,(c+l),(h+l)])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d

                        d=[]
                        # do left-hand diagonal, down height
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[r,(c-l),(h+l)])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
                            
                        d=[]
                        # do left-hand diagonal, down height
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[(r+l),c,(h+l)])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d
                        d=[]
                        
                        # do left-hand diagonal, down height
                        keep=True
                        for l in range(length):
                            try:
                                d.append(self[(r-l),c,(h+l)])
                            except IndexError:
                                keep=False
                                break
                        if keep:
                            yield d


        else:
            raise ValueError("Not implemented for dims 4+")

    def show_locations(self):
        loc=Board(*self.shape)
        loc.board=list(range(prod(self.shape)))
        print(loc)
        
    def __repr__(self):
        if not self.pieces is None:
            if any([x>=len(self.pieces) for x in self.board]):
                print("Warning...illegal values for pieces...resetting pieces")
                self.pieces=None
    
        if self.dimension==1 or self.dimension==2:
            s=""
            for row in self.rows():
                for val in row:
                    if not self.pieces is None:
                        val=self.pieces[val]
                        s+="%2s " % (val)
                    else:
                        s+="%2d " % (val)
                s+="\n"
            return s
        elif self.dimension==3:
            s=""
            for h in range(self.shape[2]):
                for r in range(self.shape[1]):
                    subs="   "*h
                    for c in range(self.shape[0]):
                        val=self[r,c,h]
                        if not self.pieces is None:
                            val=self.pieces[val]
                            subs+="%2s " % (val)
                        else:
                            subs+="%2d " % (val)
                    s+=subs+"\n"
                s+="\n"
            return s   
        else:
            s="""Shape %s
            %s""" % (str(self.shape),str(self.board))
            return str(self.board)
if __name__=="__main__":
    import random
    
    b=Board(4,4)
    b.board=list(range(len(b.board)))
    
    print(b)
    print("==")
    
    if False:
        for d in b.diags(3):
            print(d)
        print("==")
    
    if False:    
        b=Board(4,4)
        b.board=list(range(len(b.board)))
        random.shuffle(b.board)
        print(b)
        for d in b.rows(2):
            print(d)
        print("==")
        for d in b.row_positions(2):
            print(d)
        print("==")
        
        
    b=Board(4,4)
    b.pieces=['.','X','O']
    for i in range(16):
        b.board[i]=random.choice([0,1,2])
                
    print(b)
    
    b.moves(1,"nex")
    
#     b2=Board(2,3,4)  # 3D breaks still
#     b2.board=range(len(b.board))
# 
#     print b2