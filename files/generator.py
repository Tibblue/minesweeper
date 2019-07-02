"""Minefield Generator package

Not yet complete, but workable.

-Generates Minefield
-Verifies/Returns some properties

TODO: Improve Minefield Class
"""

from random import randint
from math import trunc


### BORDERs check
def isBorder(width,height,x,y):
  """True if square is at the Border

  Border is a square at the Side OR Corner
  """

  if isCorner(width,height,x,y):
    return isCorner(width,height,x,y)
  elif isSide(width,height,x,y):
    return isSide(width,height,x,y)
  else:
    return False

def isCorner(width,height,x,y):
  """True if square is at a Corner"""

  pos = x+y*width
  if (pos==0):
    return 'UL'
  elif (pos==width-1):
    return 'UR'
  elif (pos==width*(height-1)):
    return 'DL'
  elif (pos==height*width-1):
    return 'DR'
  return False

def isSide(width,height,x,y):
  """True if square is at the Side of the matrix

  Side DOES NOT include corners.
  """

  if isCorner(width,height,x,y):
    return False
  elif (x==0):
    return 'L'
  elif (x==width-1):
    return 'R'
  elif (y==0):
    return 'U'
  elif (y==height-1):
    return 'D'
  return False



class Minefield:
  """Minefield Matrix

  This matrix represents the minesweeper Minefield.

  Attributes
  ----------
  width : int
    width of the matrix
  height : int
    height of the matrix
  nMines : int
    Number of Mines in the Minefield
  posMines : Set List
    List with the positions of the mines
  matrixTuples : Matrix
    Matrix where each position is a Tuple (Status,Number)

  NOTES:
    -> Coord(x,y) = Position(x+y*width)
    Each cell/square is a Tuple (Status,Number).
      -> status - (flaged -1/hidden 0/visible 1)
      -> number - square number (or -1 for mines)


  TODO: move remaining function to the class
  """

  def __init__(self,width,height,nMines):
    self.newMinefield(width,height,nMines)

  def newMinefield(self,width,height,nMines):
    """Generate new Minefield (with given params)

    Uses the given Width, Height and Number of Mines
    to generate a new Minefield
    """

    self.width = width
    self.height = height
    self.nMines = nMines
    self.posMines = self._generateMines(width,height,nMines)
    self.matrixTuples = self._generateMatrix(width,height,self.posMines)


  def click(self,x,y,expand):
    """(Left) Click - Reveal square

    returns -1 if a mine was clicked = lost
            0 if a empty square was clicked = expands if expand=True
            1 if a number square was clicked = reveal square
            2 if a flag was clicked = do nothing
    """

    square = self.matrixTuples[y][x]
    if square[0]==-1: # flaged square
      return 2
    self.matrixTuples[y][x] = (1,square[1]) # reveals square
    if square[1]==-1: # mine square
      return -1
    if square[1]==0: # empty square
      if expand:
        if self.isSquare(x-1,y-1):
          if self.matrixTuples[y-1][x-1][0]==0 : self.click(x-1,y-1,expand=True)
        if self.isSquare(x-1,y):
          if self.matrixTuples[y][x-1][0]==0 : self.click(x-1,y,expand=True)
        if self.isSquare(x-1,y+1):
          if self.matrixTuples[y+1][x-1][0]==0 : self.click(x-1,y+1,expand=True)
        if self.isSquare(x,y-1):
          if self.matrixTuples[y-1][x][0]==0 : self.click(x,y-1,expand=True)
        if self.isSquare(x,y+1):
          if self.matrixTuples[y+1][x][0]==0 : self.click(x,y+1,expand=True)
        if self.isSquare(x+1,y-1):
          if self.matrixTuples[y-1][x+1][0]==0 : self.click(x+1,y-1,expand=True)
        if self.isSquare(x+1,y):
          if self.matrixTuples[y][x+1][0]==0 : self.click(x+1,y,expand=True)
        if self.isSquare(x+1,y+1):
          if self.matrixTuples[y+1][x+1][0]==0 : self.click(x+1,y+1,expand=True)
      return 0
    if square[1]>=1: # number square
      return 1

  def flag(self,x,y):
    """(Right) Click - Flag square

    Also unflags, flaged squares.
    """

    square = self.matrixTuples[y][x]
    if square[0]==0:
      self.matrixTuples[y][x] = (-1,square[1])
    elif square[0]==-1:
      self.matrixTuples[y][x] = (0,square[1])

  def checkVictory(self):
    """Verifies victory condictions

    Victory condictions:
      -> ALL mines must be flaged
      -> ONLY the mines must be flaged
    """

    nMinesPlaced = nMinesCorrect = 0
    for line in self.matrixTuples:
      for (status,number) in line:
        if status == -1:
          nMinesPlaced += 1
          if number == -1:
            nMinesCorrect += 1

    if nMinesPlaced == nMinesCorrect == len(self.posMines):
      return True
    return False


  def isSquare(self,x,y):
    """Check if square is inside the Minefield

    A square with Coord(7,3) in a Minefield of width 5 is not considered
    a square because its outside the boundaries.
    """

    if (x>=0 and x<self.width) and (y>=0 and y<self.height):
      return True
    return False


  # FIXME: use self vars
  def _generateMines(self,width,height,nMines):
    """Generates random positions for mines"""

    posMines = set()
    while len(posMines)<nMines:
      posMines.add(randint(0,width*height-1))
    return posMines

  # FIXME: use self vars
  def _generateMatrix(self,width,height,posMines):
    """Generates Minefield with square status and numbers

    Each square in the matrix is a tuple
    Tuple = (Status, Number)
      -> status - (flaged -1/hidden 0/visible 1)
      -> number - square number (or -1 for mines)
    """

    matrix = [j for j in range(height)]
    for j in matrix:
      matrix[j] = [i for i in range(width)]
      for i in matrix[j]:
        if i+j*width in posMines:
          matrix[j][i] = (0,-1)
        else:
          matrix[j][i] = (0,self._calculateNumber(width,height,i,j,posMines))
    return matrix

  # FIXME: use self vars
  def _calculateNumber(self,width,height,x,y,posMines):
    """Calculate Numbers a square

    Numbers are the number of adjacent mines to the square
    """

    # 8 vars, one for each adjacent square
    UL = (x-1,y-1)
    U = (x,y-1)
    UR = (x+1,y-1)
    L = (x-1,y)
    R = (x+1,y)
    DL = (x-1,y+1)
    D = (x,y+1)
    DR = (x+1,y+1)
    adjacentSquares = [UL,U,UR,L,R,DL,D,DR]

    nMinesAdjacent = 0
    for (i,j) in adjacentSquares:
      # FIXME: use isSquare in this if
      if (i>=0 and i<width) and (j>=0 and j<height):
        if i+j*width in posMines:
          nMinesAdjacent += 1
    return nMinesAdjacent



if __name__ == "__main__":
  print("All good")
