"""Matrix Generator package

Not yet complete, but workable.

-Generates Matrix
-Verifies/Returns some properties

TODO: Make Matrix a Class
"""

from random import randint
from math import trunc

### GENERATORS
def generateMines(width,height,nMines):
  """Generates random positions for mines"""

  posMines = set()
  while len(posMines)<nMines:
    posMines.add(randint(0,width*height-1))
  return posMines

def generateNumberMatrix(width,height,posMines):
  """Generates Matrix with numbers

  Each square in the matrix is a number
    -> -1 = Mines
    -> any other number - number of adjacent mines
  """

  matrix = [j for j in range(height)]
  for j in matrix:
    matrix[j] = [i for i in range(width)]
    for i in matrix[j]:
      if i+j*width in posMines:
        matrix[j][i] = -1
      elif isBorder(width,height,i,j):
        matrix[j][i] = calculateNumberBorder(width,height,i,j,posMines)
      else:
        matrix[j][i] = calculateNumberCenter(width,height,i,j,posMines)
  # for j in range(len(matrix)): # debug matrix print
  #   print(matrix[j]) # debug matrix print
  return matrix

def generateTupleMatrix(width,height,matrix):
  """Generates Matrix with square status and numbers

  Each square in the matrix is a tuple
  Tuple = (Status, Number)
    -> status - (hidden/visible)
    -> number - square number (or -1 for mines)
  """

  finalMatrix = [j for j in range(height)]
  for j in finalMatrix:
    finalMatrix[j] = [i for i in range(width)]
    for i in finalMatrix[j]:
      if matrix[j][i]==-1:
        finalMatrix[j][i] = (0,-1)
      else:
        finalMatrix[j][i] = (0,matrix[j][i])
  # for j in range(len(finalMatrix)): # debug finalMatrix print
  #   print(finalMatrix[j]) # debug finalMatrix print
  return finalMatrix

def newMinefield(width,height,nMines):
  """Generate new Minefield (with given params)

  Uses the given Width, Height and Number of Mines
  to generate a new Minefield
  """

  posMines = generateMines(width,height,nMines)
  matrix = generateNumberMatrix(width,height,posMines)
  matrixTuples = generateTupleMatrix(width,height,matrix)
  return (matrixTuples,posMines)


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


### CALCULATE NUMBERS
def calculateNumberCenter(width,height,x,y,posMines):
  """Calculate Numbers for center squares

  Numbers are the number of adjacent mines to the square
  Calculates numbers for squares not at the Border (Center)
  """

  pos = x+y*width
  nMinesAdjacent = 0
  # aux vars - squares around
  UL = pos-width-1
  U = pos-width
  UR = pos-width+1
  L = pos-1
  R = pos+1
  DL = pos+width-1
  D = pos+width
  DR = pos+width+1

  centerAdjacentSquares = [UL,U,UR,L,R,DL,D,DR]
  # print(centerAdjacentSquares) # debug
  for i in centerAdjacentSquares:
    if i in posMines:
      nMinesAdjacent += 1
  return nMinesAdjacent

def calculateNumberBorder(width,height,x,y,posMines):
  """Calculate Numbers for border squares

  Numbers are the number of adjacent mines to the square
  Calculates numbers for squares at the Border
  """

  nMinesAdjacent = 0
  # aux vars - squares around
  UL = (x-1,y-1)
  U = (x,y-1)
  UR = (x+1,y-1)
  L = (x-1,y)
  R = (x+1,y)
  DL = (x-1,y+1)
  D = (x,y+1)
  DR = (x+1,y+1)

  centerAdjacentSquares = [UL,U,UR,L,R,DL,D,DR]
  # print(centerAdjacentSquares)
  for (i,j) in centerAdjacentSquares:
    if (i>=0 and i<width) and (j>=0 and j<height):
      if i+j*width in posMines:
        nMinesAdjacent += 1
  return nMinesAdjacent


### Aux Functions for Matrix
def matrixWidth(matrix):
  return len(matrix[0])

def matrixHeight(matrix):
  return len(matrix)



if __name__ == "__main__":
  print("All good")
