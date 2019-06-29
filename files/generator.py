from random import randint
from math import trunc

### GENERATORS
# Generates random positions for mines
def generateMines(largura,altura,nMines):
  posMines = set()
  while len(posMines)<nMines:
    posMines.add(randint(0,largura*altura-1))
  # print(posMines, len(posMines)) # debug
  return posMines

# Generate Matrix with mines and numbers in place
#   -1 => mines
#   anything else is the number of adjacent mines
def generateMinesMatrix(largura,altura,posMines):
  matrix = [j for j in range(altura)]
  for j in matrix:
    matrix[j] = [i for i in range(largura)]
    for i in matrix[j]:
      if i+j*largura in posMines:
        matrix[j][i] = -1
      elif isBorder(largura,altura,i,j):
        matrix[j][i] = calculateNumberBorder(largura,altura,i,j,posMines)
      else:
        matrix[j][i] = calculateNumberCenter(largura,altura,i,j,posMines)
  # for j in range(len(matrix)): # debug matrix print
  #   print(matrix[j]) # debug matrix print
  return matrix

# Generate Final Matrix with mines and numbers hidden
#   creates a tuple with value and status (hidden/visible)
#   for each cell of the minesMatrix
def generateMinesMatrixFinal(largura,altura,matrix):
  finalMatrix = [j for j in range(altura)]
  for j in finalMatrix:
    finalMatrix[j] = [i for i in range(largura)]
    for i in finalMatrix[j]:
      if matrix[j][i]==-1:
        finalMatrix[j][i] = (0,-1)
      else:
        finalMatrix[j][i] = (0,matrix[j][i])
  # for j in range(len(finalMatrix)): # debug finalMatrix print
  #   print(finalMatrix[j]) # debug finalMatrix print
  return finalMatrix

# Generate new Minefield (with given params)
def newMinefield(largura,altura,nMines):
  posMines = generateMines(largura,altura,nMines)
  matrix = generateMinesMatrix(largura,altura,posMines)
  matrixTup = generateMinesMatrixFinal(largura,altura,matrix)
  return (matrixTup,posMines)


### BORDERS
# returns if square is at the Border (Side OR Corner)
def isBorder(largura,altura,x,y):
  if isCorner(largura,altura,x,y):
    return isCorner(largura,altura,x,y)
  elif isSide(largura,altura,x,y):
    return isSide(largura,altura,x,y)
  else:
    return False

# returns if square is at a Corner
def isCorner(largura,altura,x,y):
  pos = x+y*largura
  if (pos==0):
    return 'UL'
  elif (pos==largura-1):
    return 'UR'
  elif (pos==largura*(altura-1)):
    return 'DL'
  elif (pos==altura*largura-1):
    return 'DR'
  return False

# returns if square is at a Side
def isSide(largura,altura,x,y):
  if isCorner(largura,altura,x,y):
    return False
  elif (x==0):
    return 'L'
  elif (x==largura-1):
    return 'R'
  elif (y==0):
    return 'U'
  elif (y==altura-1):
    return 'D'
  return False


### CALCULATE NUMBERS
# Calculate Numbers for center squares (number of adjacent mines)
def calculateNumberCenter(largura,altura,x,y,posMines):
  pos = x+y*largura
  nMinesAdjacent = 0
  # aux vars - squares around
  UL = pos-largura-1
  U = pos-largura
  UR = pos-largura+1
  L = pos-1
  R = pos+1
  DL = pos+largura-1
  D = pos+largura
  DR = pos+largura+1

  centerAdjacentSquares = [UL,U,UR,L,R,DL,D,DR]
  # print(centerAdjacentSquares) # debug
  for i in centerAdjacentSquares:
    if i in posMines:
      nMinesAdjacent += 1
  return nMinesAdjacent

# Calculate Numbers for border squares (number of adjacent mines)
def calculateNumberBorder(largura,altura,x,y,posMines):
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
    if (i>=0 and i<largura) and (j>=0 and j<altura):
      if i+j*largura in posMines:
        nMinesAdjacent += 1
  return nMinesAdjacent



### Aux Functions for Matrix
def matrixWidth(matrix):
  return len(matrix[0])

def matrixHeight(matrix):
  return len(matrix)



if __name__ == "__main__":
  print("All good")
