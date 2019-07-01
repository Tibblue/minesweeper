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



### CLICKs
def click(x,y,matrix):
  """(Left) Click - Reveal square

  returns -1 if a mine was clicked = lost
           0 if a empty square was clicked = expand surroundings (TODO)
           1 if a number square was clicked = show square
           2 if a flag was clicked = do nothing
  """

  square = matrix[y][x]
  if square[0]==-1: # flaged square
    return 2
  matrix[y][x] = (1,square[1]) # reveals square
  if square[1]==-1: # mine square
    return -1
  if square[1]==0: # empty square
    return 0
  if square[1]>=1: # number square
    return 1

def flag(x,y,matrix):
  """(Right) Click - Flag square

  Also unflags, flaged squares.
  """

  square = matrix[y][x]
  if square[0]==0:
    matrix[y][x] = (-1,square[1])
  elif square[0]==-1:
    matrix[y][x] = (0,square[1])

def checkVictory(matrix,posMines):
  """Verifies victory condictions

  Victory condictions:
    -> All mines must be flaged
    -> Remaining flags = 0 (TODO)

  FIXME: only win when only the mines are flaged, and no excess
         flags where placed.
  """

  largura = matrixWidth(matrix)
  altura = matrixHeight(matrix)
  nMinesLeft = len(posMines)
  for i in posMines:
    x = i % largura
    y = trunc(i / largura)
    # print(x,y) # debug
    square = matrix[y][x]
    # print(square) # debug
    if square[0]==-1:
      nMinesLeft -= 1

  # print(nMinesLeft)
  if nMinesLeft==0:
    return True
  return False


### Aux Functions for Matrix
def matrixWidth(matrix):
  return len(matrix[0])

def matrixHeight(matrix):
  return len(matrix)



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


  def _generateMines(self,width,height,nMines):
    """Generates random positions for mines"""

    posMines = set()
    while len(posMines)<nMines:
      posMines.add(randint(0,width*height-1))
    return posMines

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
      if (i>=0 and i<width) and (j>=0 and j<height):
        if i+j*width in posMines:
          nMinesAdjacent += 1
    return nMinesAdjacent



if __name__ == "__main__":
  print("All good")
