#!/usr/bin/env python3
"""Minesweeper Generator package

  Almost complete, but room for aditions and improvements.

  -Generates Minefield
  -Verifies/Returns some properties

  TODO: Improve Minesweeper Class
  TODO: add ranking, and in-game timer
"""

from random import randint


class Minesweeper:
  """Minesweeper generator Class

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
      This matrix represents the Minesweeper Minefield.
      Matrix where each position is a Tuple (Status,Number)
    firstClick : Boolean
      Is True if player didnt click yet (next click is the first)

    NOTES:
      -> Coord(x,y) = Position(x+y*width)
      Each cell/square is a Tuple (Status,Number).
        -> status - (flaged -1/hidden 0/visible 1)
        -> number - square number (or -1 for mines)

    TODO: move remaining functions to the class
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
    self.posMines = self._generateMines()
    self.matrixTuples = self._generateMatrix()
    self.firstClick = True


  def click(self,x,y,expand):
    """(Left) Click - Reveal square

      returns -2 if a mine was clicked on the first click =
                    should generate a new map
              -1 if a mine was clicked = lost
              0 if a empty square was clicked = expands if expand=True
              1 if a number square was clicked = reveal square
              2 if a flag was clicked = do nothing
    """

    square = self.matrixTuples[y][x]
    if self.firstClick:
      self.firstClick = False
      if square[1]==-1:
        return -2 # mine on first square
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


  def _generateMines(self):
    """Generates random positions for mines"""

    posMines = set()
    while len(posMines)<self.nMines:
      posMines.add(randint(0,self.width*self.height-1))
    return posMines

  def _generateMatrix(self):
    """Generates Minefield with square status and numbers

      Each square in the matrix is a tuple
      Tuple = (Status, Number)
        -> status - (flaged -1/hidden 0/visible 1)
        -> number - square number (or -1 for mines)
    """

    matrix = [j for j in range(self.height)]
    for j in matrix:
      matrix[j] = [i for i in range(self.width)]
      for i in matrix[j]:
        if i+j*self.width in self.posMines:
          matrix[j][i] = (0,-1)
        else:
          matrix[j][i] = (0,self._calculateNumber(i,j))
    return matrix

  def _calculateNumber(self,x,y):
    """Calculate Numbers for a square

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
      if (i>=0 and i<self.width) and (j>=0 and j<self.height):
        if i+j*self.width in self.posMines:
          nMinesAdjacent += 1
    return nMinesAdjacent



if __name__ == "__main__":
  print("All good")
