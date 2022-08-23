import numpy as np

class Node ():
  def __init__(self, state,value,operators,operator=None, parent=None,objective=None):
    self.state= state
    self.value = value
    self.children = []
    self.parent=parent
    self.operator=operator
    self.objective=objective
    self.level=0
    self.operators=operators
    self.v=0

  def add_child(self, value, state, operator):
    node=type(self)(value=value, state=state, operator=operator,parent=self,operators=self.operators)
    node.level=node.parent.level+1
    self.children.append(node)
    return node
  
  def add_node_child(self, node):
    node.level=node.parent.level+1
    self.children.append(node)    
    return node

  def getchildrens(self):
    return [
        self.getState(i) 
          if not self.repeatStatePath(self.getState(i)) 
            else None for i, op in enumerate(self.operators)]

  def getState(self, index):
    pass

  #Qué son eq y it?
  def __eq__(self, other):
    return self.state == other.state
 
  def __lt__(self, other):
    return self.f() < other.f()
   
  def repeatStatePath(self, state):
      n=self
      while n is not None and n.state!=state:
          n=n.parent
      return n is not None
    
  def pathObjective(self):
      n=self
      result=[]
      while n is not None:
          result.append(n)
          n=n.parent
      return result
  
  def heuristic(self):
    return 0
  
  def cost(self):
    return 1

  def f(self): 
    return self.cost()+self.heuristic()

  def isObjective(self):
    return (self.state==self.objetive.state)

class Tree ():
  def __init__(self, root ,operators):
    self.root=root
    self.operators=operators

  def reinitRoot(self):
    self.root.operator=None
    self.root.parent=None
    self.root.objective=None
    self.root.children = []
    self.root.level=0
    
  def miniMax(self, depth):
    self.root.v=self.miniMaxR(self.root, depth, self.root.player)
    ## Comparar los hijos de root
    values=[c.v for c in self.root.children]
    if self.root.player:
      maxvalue=max(values)
      index=values.index(maxvalue)
    else:
      minValue=min(values)
      index=values.index(minValue)

    return self.root.children[index]

  def miniMaxR(self, node, depth, maxPlayer):
    #Condición de parada
    if depth==0 or node.isObjective():
      node.v=node.heuristic()
      return node.heuristic()
    ## Generar los hijos del nodo
    children=node.getchildrens()
    
    ## Según el jugador que sea en el árbol
    if maxPlayer:
      value=float('-inf')
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, 
                                   operators=node.operators,player=False)
          newChild=node.add_node_child(newChild)
          value=max(value,self.miniMaxR(newChild,depth-1,False))
    else:
      value=float('inf')
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node,
                                   operators=node.operators,player=True)
          newChild=node.add_node_child(newChild)
          value=min(value,self.miniMaxR(newChild,depth-1,True))
    node.v=value
    return value

  def alpha_beta(self, depth):
    self.root.v= self.alpha_betaR(self.root, depth, float('-inf'), float('+inf'), self.root.player)
    values=[c.v for c in self.root.children]
    if self.root.player:
      maxvalue=max(values)
      index=values.index(maxvalue)
    else:
      minValue=min(values)
      index=values.index(minValue)

    return self.root.children[index]
 
  def alpha_betaR(self, node, depth, alpha, beta, player):
    if depth == 0 or node.isObjective():
       node.v = node.heuristic()
       return node.heuristic()
    if player:
      value=float('-inf')
      children = node.getchildrens()
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, operators=node.operators,player=False)
          newChild=node.add_node_child(newChild)
          value = max(value,self.alpha_betaR(newChild, depth-1, alpha,beta,False))
          alpha = max(alpha,value)
          if alpha>=beta:
            break
     
    else:
      value=float('inf')
      children = node.getchildrens()
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, operators=node.operators,player=True)
          newChild=node.add_node_child(newChild)
          value = min(value,self.alpha_betaR(newChild, depth-1, alpha,beta,True))
          beta = min(beta,value)
          if alpha>=beta:
            break
    node.v = value
    return value

class NodeConnectFour(Node):

  def __init__(self, player=True,**kwargs):
    super(NodeConnectFour, self).__init__(**kwargs)
    self.player=player
    if player:
      self.v=float('-inf')
    else:
      self.v=float('inf')

  def getState(self, index):
    state=self.state
    
    #If the column's last position is not empty, the play is ilegal
    if state[0][index] != 0:
      return None

    nextState=[r.copy() for r in state]
    #Reverse the state so its more efficient in the first plays (more common and more childrens, more used)
    nextState.reverse()
    lastEmpty = -1
    #We check what is the next possible play in the column (index) given
    for i, row in enumerate(nextState):
      if row [index] == 0:
        lastEmpty = i
        break
    #If lastEmpty wasn't modified that means the column is full of 0s. Then the play can be done in the first available position
    if lastEmpty == -1:
      lastEmpty = 0
    
    nextState[lastEmpty][index] = 1 if self.player else 2
    nextState.reverse()

    return nextState if state!=nextState else None


  def cost(self):
    return self.level
  
  def isObjective (self):
    board = np.array(self.state)
    rows, columns =  board.shape
    
    piece = 1
    for piece in range (2):
      piece += 1
    #Check horizontal locations
      for c in range (columns - 3):
        for r in range (rows):
          if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
            return True

      #Check vertical locations
      for c in range (columns):
        for r in range (rows-3):
          if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
            return True

      #Check positively sloped diagonals
      for c in range (columns-3):
        for r in range (rows-3):
          if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
            return True

      #Check negatively sloped diagonals
      for c in range (columns-3):
        for r in range (3, rows):
          if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
            return True

    #If there is no victory, we check if the whole board is full (tie)
    aux_board = board != 0
    if aux_board.all():
      return True

    return False

  def get_score(self, four, piece):
    if piece==1:
      op=2
    else:
      op=1
    score=0

    if four.count(piece)==4:
      return float('inf')
    elif four.count(op)==4:
      return float('-inf')

    if four.count(piece)==3 and four.count(0)==1:
      score+=50000
    elif four.count(piece)==2 and four.count(0)==2:
      score+=5000
    elif four.count(piece)==1 and four.count(0)==3:
      score+=500

    if four.count(op)==3 and four.count(0)==1:
      score-=10000
    elif four.count(op)==2 and four.count(0)==2:
      score-=1000
    elif four.count(op)==1 and four.count(0)==3:
      score-=100
    return score

  def heuristic(self):
    board = self.state
    
    piece = 1
    board = np.array(board)
    rows, columns =  board.shape
    
    score=0

    #Check horizontal locations
    for c in range (columns - 3):
      for r in range (rows):
        four=[board[r][c],board[r][c+1],board[r][c+2],board[r][c+3]]
        score+=self.get_score(four, piece)
    
    #Check vertical locations
    for c in range (columns):
      for r in range (rows-3):
        four=[board[r][c],board[r+1][c],board[r+2][c],board[r+3][c]]
        score+=self.get_score(four,piece)

    #Check positively sloped diagonals
    for c in range (columns-3):
      for r in range (rows-3):
        four=[board[r][c],board[r+1][c+1],board[r+2][c+2],board[r+3][c+3]]
        score+=self.get_score(four,piece)

    #Check negatively sloped diagonals
    for c in range (columns-3):
      for r in range (3, rows):
        four=[board[r][c],board[r-1][c+1],board[r-2][c+2],board[r-3][c+3]]
        score+=self.get_score(four,piece)
    
    
    #return score*-1 if self.player else score
    return score

  def printBoard (self, board):
    for i, r in enumerate (board):
      print (r)
    return 0


