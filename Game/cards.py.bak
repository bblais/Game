import random

class Card(object):

    def __init__(self,rank,suit):
        self.rank=rank
        self.suit=suit
        self.__initialized=True

    def __deepcopy__(self,memo):
        newcard=Card(self.rank,self.suit)
        return newcard

    def _color(self):
        if self.suit=='Spades' or self.suit=='Clubs':
            return 'Black'
        elif self.suit=='Hearts' or self.suit=='Diamonds':
            return 'Red'
        else:
            return None

    def __hash__(self):
        return hash(str(self))  #  allow it in a dictionary        

    def __getattr__(self,item):
        if item=='color':
            return self._color()
            
        if item=='isface':
            return self.rank==11 or self.rank==12 or self.rank==13
        
        raise AttributeError

    def __setattr__(self,item,value):
        if item=='suit':
            suits={'h':'Hearts','s':'Spades','d':'Diamonds','c':'Clubs',
                    'j':'Joker','n':None}
            if not value is None:                
                value=suits[value.lower()[0]]

        if not self.__dict__.has_key('_Card__initialized'):  
            # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item): 
            # any normal attributes are handled normally            
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

                        
    def __repr__(self):
        if self.rank==1:
            rankstr='Ace'
        elif self.rank==11:
            rankstr='Jack'
        elif self.rank==12:
            rankstr='Queen'
        elif self.rank==13:
            rankstr='King'
        elif self.rank is None:
            rankstr='Nothing'
        else:
            rankstr='%d' % self.rank
            
        if self.suit=='Joker':
            s='Joker'
        elif self.suit is None:
            s=rankstr
        else:
            s='%s of %s' % (rankstr,self.suit)
        
        return s
        
    def match(self,other):
        if self==other:
            return True
            
        if (self.rank==None or other.rank==None) and self.suit==other.suit:
            return True
            
        if (self.suit==None or other.suit==None) and self.rank==other.rank:
            return True
        
        # None, None matches all
        if self.suit==None and self.rank==None:
            return True
    
        if other.suit==None and other.rank==None:
            return True
    
        return False
        
    def __gt__(self,other):
        return self.rank>other.rank
        
    def __lt__(self,other):
        return self.rank<other.rank
        
    def __ge__(self,other):
        return self.rank>=other.rank
        
    def __le__(self,other):
        return self.rank<=other.rank
    
    def __eq__(self,other):
        return self.rank==other.rank and self.suit==other.suit
        
def translate(cardval):
    if isinstance(cardval,Card):
        return cardval
        
    if isinstance(cardval,int):  # rank given
        return Card(cardval,None)
        
        
    parts=cardval.split('of')
    parts=[p.strip() for p in parts]

    if len(parts)>1:
        suits={'h':'Hearts','s':'Spades','d':'Diamonds','c':'Clubs',
                'j':'Joker','n':None}
        suit=suits[parts[1].lower()[0]]
    else:
        suit=None
    
    try:
        rank=int(parts[0])
    except ValueError:  # not an int...perhaps like "ace", or a suit?
        ranks={'a':1,'j':11,'q':12,'k':13,'n':None}
        
        try:
            rank=ranks[parts[0].lower()[0]]
        except KeyError:
            rank=None
            suits={'h':'Hearts','s':'Spades','d':'Diamonds','c':'Clubs',
                    'j':'Joker','n':None}
            suit=suits[parts[0].lower()[0]]
        
        
    return Card(rank,suit)


class CardList(list):
    def __hash__(self):
        return hash(str(self))  #  allow it in a dictionary        

    def find(self,cards):

        if not isinstance(cards,list):
            cards=[cards]
        
        result=[]
        for card1 in cards:
            for card2 in self:
                other=translate(card1)            
                if other.match(card2):
                    if card2 not in result:
                        result.append(card2)
        
                
        return result

    def deal(self,N=1):
        hand=CardList()
        for i in range(N):
            hand.append(self.pop(0))
        return hand
        
   
class Hand(CardList):
    pass
class Deck(CardList):
    pass
    
def deal(deck,N=1):
    hand=CardList()
    for i in range(N):
        hand.append(deck.pop(0))
    return hand


def draw(deck,N=1,replace=False):
    hand=CardList()
    
    if not replace:
        for i in range(N):
            hand.append(deck.pop(0))
    else:
        for i in range(N):
            hand.append(random.choice(deck))
            
    return hand


def makedeck(N=1,shuffle=True,joker=0):
    deck=CardList()
    for i in range(N):
        for suit in ['hearts','clubs','spades','diamonds']:
            for rank in range(1,13+1):
                deck.append(Card(rank,suit))
                
    for j in range(joker):
        deck.append(Card(0,'joker'))
                
    if shuffle:
        random.shuffle(deck)
        
    return deck
