def prod(A):
    p=1
    for val in A:
        p*=val
    return p

try:
    from numpy import int64
except ImportError:
    int64 = int

"""
List is a subclass of the built-in list class in Python. It allows for conversion to an immutable tuple and hashing.

Example:
lst = List([1, 2, 3])
# Convert to immutable tuple
tpl = lst.immutable() # returns (1, 2, 3)
# Hash the list
hsh = hash(lst) # returns a unique hash value for the list

"""

class List(list):

    def immutable(self):
        """
        Returns an immutable tuple copy of the list.

        Returns:
            tuple: An immutable tuple copy of the list.
        """
        return tuple(self)

    def __hash__(self):
        """
        Returns a hash value for the list.

        Returns:
            int: A unique hash value for the list.
        """
        return hash(tuple(self))

class Board(object):
    """
    A class for representing a board with various dimensions and pieces.

    Args:
        *args: The dimensions of the board.

    Attributes:
        shape (tuple): The shape of the board.
        dimension (int): The number of dimensions of the board.
        board (list): A list containing the values at each position on the board.
        pieces (None): Placeholder for future implementation to add different types of pieces to the board.
        team (dict): A dictionary mapping player numbers to team numbers.

    Methods:
        __eq__(other): Compares two boards to see if they are equal.
        __int__(): Converts a board to an integer value, useful for hashing.
        immutable(): Returns an immutable tuple representation of the current state of the board.
        __len__(): Returns the number of positions on the board.
        find(player): Returns a list containing all positions on the board where a certain player's piece is located.
        index_from_rc(rc,c=None): Converts row-column coordinates or strings ("A1") or integers to an index in the one-dimensional array representing the board. Raises IndexError if row or column is out of bounds, or if index is out of bounds for one-dimensional boards. Raises ValueError if more than three dimensions are present in shape.
        rc_from_index(index): Converts an index in a one-dimensional array representing the board to row-column coordinates or tuples. Raises ValueError if more than three dimensions are present in shape.
        __getitem__(key): Gets the value at a specific position on the board using row-column coordinates or strings ("A1") or integers as input.
        __setitem__(key,val): Sets a specific position on the board using row-column coordinates or strings ("A1") or integers as input and assigning val as its value.
        row_positions(length=None): Yields all possible positions for rows with length specified by the length parameter. 

        Example:
        board = Board(3,3)
        board[0] = 1
        board[4] = 2
        assert board.find(1) == [0]
        assert board.find(2) == [4]

    """

    def __init__(self,*args):
        if isinstance(args[0],str):
            board_str=args[0]
            num_rows=board_str.count("/")+1
            b=[int(_) for _ in ''.join([line.strip() for line in board_str.strip().split('/')])]
            num_cols=len(b)//num_rows

            self.shape=(num_rows,num_cols)
            self.board=b

        else:
            self.shape=args
            self.board=[0]*prod(args)


        self.dimension=len(self.shape)
        self.pieces=None
        self.team={}
        for i in range(3):
            self.team[i]=i
        
    def __eq__(self,other):
        try:
            return other.board==self.board
        except AttributeError:
            return False

    def __int__(self):
        N=9  # first digit
        for v in self.board:
            N=N*10+v
            
        return N
    

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
        
    def location(self,r,c):
        return self.index_from_rc(r,c)
    def row(self,location):
        r,c=self.rc_from_index(location)
        return r

    def col(self,location):
        r,c=self.rc_from_index(location)
        return c
    
    def index_from_rc(self,rc,c=None):
    	# Convert row-column coordinates to list format if c argument is provided.

        
        if not c is None:
            rc=[rc,c]

    	# Convert strings representing row-column coordinates to integer format.
        if isinstance(rc,str):
            rc=[int(rc[1:])-1,ord(rc[0])-97]

    	# Convert integers to index if only one argument is provided.
        if isinstance(rc,(int,int64)):
            index=rc
            if rc>=len(self.board) or rc<0:
                raise IndexError("Illegal index")

    	# Convert coordinates to index for one-dimensional boards.
        elif len(self.shape)==1:
            index=rc[0]
            if index>=length(self.board) or rc<0:
                raise IndexError("Illegal index")

    	# Convert coordinates to index for two-dimensional boards.
        elif len(self.shape)==2:
            r,c=rc
            
            if r>=self.shape[0] or r<0:
                raise IndexError("Illegal row")
            if c>=self.shape[1] or c<0:
                raise IndexError("Illegal col")
                
            index=r*self.shape[1]+c

    	# Convert coordinates to index for three-dimensional boards.
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
        """
        Converts a linear index to a row-column pair for a 2D or 3D board.
        If the input is a list of indices, returns a list of row-column pairs.

        Parameters:
        index (int or list): The linear index or list of linear indices to be converted.

        Returns:
        tuple or list of tuples: A tuple representing the row and column for a 2D board,
                                or a tuple representing the height, row, and column for a 3D board,
                                or a list of such tuples if the input is a list.
                                
        Raises:
        ValueError: If the shape of the board is not 1D, 2D, or 3D.
                    If the input index is out of range for a 1D board.
        """

        if isinstance(index,list):
            rc=[self.rc_from_index(i) for i in index]
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
        """
        Generates all possible positions for rows of length `length` in this board.

        Parameters:
        length (int): The number of positions in each row to generate.
                    If None, generates all possible rows of maximum length given this board's shape.
                    
        Yields:
        list: A list of tuples representing positions in one row of this board. 
            Each tuple represents a position as an index.
            
            For example, if this is a 2D board with shape (3,4) and length=2, the generator
            will yield the following rows:
            
            [0, 1]
            [1, 2]
            [2, 3]
            [4, 5]
            [5, 6]
            [6, 7]
            [8, 9]
            [9, 10]
            [10, 11]            

        """
        
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for row in tempboard.rows(length):
            yield row

    def _get_moves(self,player,m):
        for i in range(max(self.board)+1):
            if i not in self.team:
                self.team[i]=i

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
                        self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                            all_moves.append( [p2,p1] )

            if m=='s':
                for col in self.col_positions(3):
                    p1,pm,p2=col  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                        self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                            all_moves.append( [p1,p2] )
            
            if m=='e':
                for row in self.row_positions(3):
                    p1,pm,p2=row  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                        self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                            all_moves.append( [p1,p2] )

            if m=='w':
                for row in self.col_positions(3):
                    p1,pm,p2=row  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p2]==player and self[p1]==0 and 
                        self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                            all_moves.append( [p2,p1] )

            if m=='ne':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p2]==player and self[p1]==0 and 
                            p2-p1==2*self.shape[1]-2 and
                            self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                        all_moves.append( [p2,p1] )

            if m=='nw':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1
                    
                    if (self[p2]==player and self[p1]==0 and 
                            p2-p1==2*self.shape[1]+2 and
                            self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                        all_moves.append( [p2,p1] )

            if m=='se':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                            p2-p1==2*self.shape[1]+2 and
                            self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                        all_moves.append( [p1,p2] )

            if m=='sw':
                for diag in self.diag_positions(3):
                    p1,pm,p2=diag  # p1 is always less than p2
                    if p1>p2:
                        p1,p2=p2,p1

                    if (self[p1]==player and self[p2]==0 and 
                            p2-p1==2*self.shape[1]-2 and
                            self[pm]!=0 and self[pm]!=player and
                        self.team[player]!=self.team[self[pm]]):
                        all_moves.append( [p1,p2] )

            return all_moves


        # no jump
        if m=='n':
            for col in self.col_positions(2):
                p1,p2=col  # p1 is always less than p2
                if p1>p2:
                    p1,p2=p2,p1
                if capture:
                    if (self[p2]==player and self[p1]!=0 and self[p1]!=player and
                        self.team[player]!=self.team[self[p1]]):
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
                    if (self[p1]==player and self[p2]!=0 and self[p2]!=player and
                        self.team[player]!=self.team[self[p2]]):
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
                    if (self[p1]==player and self[p2]!=0 and self[p2]!=player and
                        self.team[player]!=self.team[self[p2]]):
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
                    if (self[p2]==player and self[p1]!=0 and self[p1]!=player and
                        self.team[player]!=self.team[self[p1]]):
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
                    if (self[p2]==player and self[p1]!=0 and self[p1]!=player 
                        and p2-p1==self.shape[1]-1 and
                        self.team[player]!=self.team[self[p1]]):
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
                    if (self[p2]==player  and self[p1]!=0 and self[p1]!=player and 
                        p2-p1==self.shape[1]+1 and
                        self.team[player]!=self.team[self[p1]]):
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
                    if (self[p1]==player and self[p2]!=0 and self[p2]!=player and 
                        p2-p1==self.shape[1]+1 and
                        self.team[player]!=self.team[self[p2]]):
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
                    if (self[p1]==player  and self[p2]!=0 and self[p2]!=player and 
                        p2-p1==self.shape[1]-1 and
                        self.team[player]!=self.team[self[p2]]):
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
        """
        Generates all possible positions for columns of length `length` in this board.

        Parameters:
        length (int): The number of positions in each col to generate.
                    If None, generates all possible cols of maximum length given this board's shape.
                    
        Yields:
        list: A list of tuples representing positions in one col of this board. 
            Each tuple represents a position as an index.
            
            For example, if this is a 2D board with shape (3,4) and length=2, the generator
            will yield the following cols:
            
            [0, 4]
            [1, 5]
            [2, 6]
            [3, 7]
            [4, 8]
            [5, 9]
            [6, 10]
            [7, 11]

        """
         
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for col in tempboard.cols(length):
            yield col
        
    def diag_positions(self,length=None):
        """
        Generates all possible positions for diagonals of length `length` in this board.

        Parameters:
        length (int): The number of positions in each diagonal to generate.
                    If None, generates all possible diagonals of maximum length given this board's shape.
                    
        Yields:
        list: A list of tuples representing positions in one diagonals of this board. 
            Each tuple represents a position as an index.
            
            For example, if this is a 2D board with shape (3,4) and length=2, the generator
            will yield the following diagonals:
            
            [0, 5]
            [1, 6]
            [1, 4]
            [2, 7]
            [2, 5]
            [3, 6]
            [4, 9]
            [5, 10]
            [5, 8]
            [6, 11]
            [6, 9]
            [7, 10]
        """
                 
        tempboard=Board(*self.shape)
        tempboard.board=list(range(prod(self.shape)))
        
        for diag in tempboard.diags(length):
            yield diag
            
    def __hash__(self):
        return hash(tuple(self.board))
        
    def rows(self,length=None):
        if self.dimension==1:
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

    def show_locations(self,notation='index'):
        """
        The show_locations method displays the locations of each cell on the board. 
        The notation parameter determines how the locations are displayed. 
        If notation is set to 'index', the locations are displayed using index notation 
        (i.e., the numbers 0 through n-1, where n is the number of cells on the board).
        If notation starts with 'alg' (short for algebraic notation), then the locations 
        are displayed using chess-like algebraic notation. The algebraic notation used 
        for a 1D board is simply "a1", "b1", "c1", etc., while for a 2D board 
        it's "a1", "b1", "c1" up to "a2", "b2", etc. If any other value is passed 
        as notation, a ValueError is raised.

        For example, if this is a 2D board with shape (3,4), the following will be dislayed:

            0  1  2  3
            4  5  6  7
            8  9 10 11        
        """

        loc=Board(*self.shape)
        loc.board=list(range(prod(self.shape)))

        if notation=='index':
            pass
        elif notation.startswith('alg'):
            if self.dimension==1:
                for i in range(len(self.board)):
                    loc[i]='%c1' % (97+i)
            elif self.dimension==2:
                p=[]
                for i in range(prod(self.shape)):
                    r,c=self.rc_from_index(i)
                    p.append('%c%d' % (97+c,self.shape[0]-r))

                loc.pieces=p
        else:
            raise ValueError("notation %s not implemented" % notation)


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