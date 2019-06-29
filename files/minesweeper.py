#!/usr/bin/env python3
# FLASK_APP=minesweeper.py FLASK_ENV=development flask run

import webbrowser

from random import randint
from math import trunc
import argparse, sys
from flask import *
app = Flask("Minesweeper")

largura = 15
altura = 5
matrix = []
matrixTup = []
posMines = {}
buttons = '''
  <script>
    function WhichButton(event,x,y) {
      // alert("xy:"+x+y+" You pressed button: " + event.button)
      if(event.button==0)
        window.location.replace("/leftClick?x="+x+"&y="+y);
      else
        window.location.replace("/rightClick?x="+x+"&y="+y);
    }
  </script>

  <button type="button">
    <a href="/newMapEasy">Generate New Map (Easy Dificulty)</a>
  </button>
  <button type="button">
    <a href="/newMapNormal">Generate New Map (Normal Dificulty)</a>
  </button>
  <button type="button">
    <a href="/newMapHard">Generate New Map (Hard Dificulty)</a>
  </button>
  <br>
  <br>
  <form method="get" action="/custom">
    Largura:
    <input type="number" name="largura" placeholder="largura">
    <br>
    Altura:
    <input type="number" name="altura" placeholder="altura">
    <br>
    Numero de Minas:
    <input type="number" name="nMines" placeholder="minas">
    <br>
    <input type="submit" value="Generate New Map (Costum Settings)">
  </form>
  <br>
'''

@app.route('/')
def play():
  if matrix == []:
    return redirect(url_for('newMapNormal'))
  html = f'<h1>{largura}x{altura} - {nMines} Minas</h1>'
  html += buttons
  html += drawField()
  html += '<br><br><br><br><br>'
  html += drawFieldOpen()
  return html

@app.route('/victory')
def victory():
  newMinefield(20,10,30)
  html = f'<h1>You Won!!!</h1>'
  html += buttons
  return html

@app.route('/lost')
def lost():
  newMinefield(20,10,30)
  html = f'<h1>You Lost</h1>'
  html += buttons
  return html

@app.route('/leftClick')
def leftClick():
  x = int(request.args.get('x'))
  y = int(request.args.get('y'))
  if click(x,y):
    if checkVictory():
      return redirect(url_for('victory'))
    else:
      return redirect(url_for('play'))
  else:
    return redirect(url_for('lost'))

@app.route('/rightClick')
def rightClick():
  x = int(request.args.get('x'))
  y = int(request.args.get('y'))
  flag(x,y)
  if checkVictory():
    return redirect(url_for('victory'))
  else:
    return redirect(url_for('play'))

@app.route('/newMapEasy')
def newMapEasy():
  newMinefield(10,8,10)
  return redirect(url_for('play'))

@app.route('/newMapNormal')
def newMapNormal():
  newMinefield(20,10,30)
  return redirect(url_for('play'))

@app.route('/newMapHard')
def newMapHard():
  newMinefield(30,20,125)
  return redirect(url_for('play'))

@app.route('/custom')
def newMapCustom():
  largura = int(request.args.get('largura'))
  altura = int(request.args.get('altura'))
  nMines = int(request.args.get('nMines'))
  newMinefield(largura,altura,nMines)
  return redirect(url_for('play'))


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
def newMinefield(larguraNew,alturaNew,nMinesNew):
  global largura, altura, nMines
  global matrixTup, matrix, posMines
  largura = larguraNew
  altura = alturaNew
  nMines = nMinesNew
  posMines = generateMines(largura,altura,nMines)
  matrix = generateMinesMatrix(largura,altura,posMines)
  matrixTup = generateMinesMatrixFinal(largura,altura,matrix)

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

# Draws HTML for the minefield
def drawField():
  global largura, altura
  global matrixTup, posMines
  # for j in range(len(matrixTup)): # debug matrixTup print
  #   print(matrixTup[j]) # debug matrixTup print

  html = '<table oncontextmenu="return false;">\n'
  for y in range(altura):
    html += '<tr>'
    for x in range(largura):
      html += '<td align="center" width="32" height="32"'
      if matrixTup[y][x][0]==0:
        html += f' id="mines" onmouseup="WhichButton(event,{x},{y})"><img src="static/images/block.jpg" alt="Mine" width="32" height="32">'
      elif matrixTup[y][x][0]==-1:
        html += f' id="mines" onmouseup="WhichButton(event,{x},{y})"><img src="static/images/flag.jpg" alt="Mine" width="32" height="32">'
      else:
        if matrixTup[y][x][1]==-1:
          html += f'><img src="static/images/mineRED.jpg" alt="Mine" width="32" height="32">'
          # html += f'><a href="/leftClick?x={x}&y={y}"><img src="static/images/mineRED.jpg" alt="Mine" width="32" height="32"></a>'
        else:
          if matrixTup[y][x][1]>4:
            html += f' style="background-color:rgb(255, 64, 64)">'
          elif matrixTup[y][x][1]==4:
            html += f' style="background-color:rgb(255, 128, 32)">'
          elif matrixTup[y][x][1]==3:
            html += f' style="background-color:rgb(224, 224, 32)">'
          elif matrixTup[y][x][1]==2:
            html += f' style="background-color:rgb(64, 192, 64)">'
          elif matrixTup[y][x][1]==1:
            html += f' style="background-color:rgb(64, 192, 255)">'
          else:
            html += f' style="background-color:rgb(192, 192, 192)">'
          html += '<p style="font-size:28px">'+str(matrixTup[y][x][1])+'</p>'
      html += '</td>'
    html += '</tr>'
  html += '</table>\n'
  return html

# Draws HTML for the minefield (all visible)
def drawFieldOpen():
  global largura, altura
  global matrixTup, posMines
  # for j in range(len(matrixTup)): # debug matrixTup print
  #   print(matrixTup[j]) # debug matrixTup print

  html = '<table>\n'
  for y in range(altura):
    html += '<tr>'
    for x in range(largura):
      html += '<td align="center" width="16" height="16"'
      if matrixTup[y][x][1]==-1:
        html += '><img src="static/images/mineRED.jpg" alt="Mine" width="16" height="16">'
      else:
        if matrixTup[y][x][1]>4:
          html += ' style="background-color:rgb(255, 64, 64);">'+str(matrixTup[y][x][1])
        elif matrixTup[y][x][1]==4:
          html += ' style="background-color:rgb(255, 128, 32);">'+str(matrixTup[y][x][1])
        elif matrixTup[y][x][1]==3:
          html += ' style="background-color:rgb(224, 224, 32);">'+str(matrixTup[y][x][1])
        elif matrixTup[y][x][1]==2:
          html += ' style="background-color:rgb(64, 192, 64);">'+str(matrixTup[y][x][1])
        elif matrixTup[y][x][1]==1:
          html += ' style="background-color:rgb(64, 192, 255);">'+str(matrixTup[y][x][1])
        else:
          html += ' style="background-color:rgb(192, 192, 192);">'+str(matrixTup[y][x][1])
      html += '</td>'
    html += '</tr>'
  html += '</table>\n'
  html += '<p>Mines Position: '+str(posMines)+'</p>' # debug
  return html

### CLICKs
# Left Click - Reveal square
# return False - clicked mine = lost
#        True - clicked number = reveal and continue
def click(x,y):
  global matrixTup
  square = matrixTup[y][x]
  if square[0]==-1: # flaged square
    return True
  matrixTup[y][x] = (1,square[1])
  if square[1]==-1: # mine square
    return False
  return True

# Right Click - Flag square
def flag(x,y):
  global matrixTup
  square = matrixTup[y][x]
  if square[0]==0:
    matrixTup[y][x] = (-1,square[1])
  elif square[0]==-1:
    matrixTup[y][x] = (0,square[1])

# Check Victory
def checkVictory():
  global largura, altura
  global matrixTup, posMines

  nMinesLeft = len(posMines)
  for i in posMines:
    x = i % largura
    y = trunc(i / largura)
    # print(x,y) # debug
    square = matrixTup[y][x]
    # print(square) # debug
    if square[0]==-1:
      nMinesLeft -= 1

  # print(nMinesLeft)
  if nMinesLeft==0:
    return True
  return False



def main():
  ### Parse Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-w','--web', action="store_true",help='Starts in Web/Browser mode (Flask server)')
  parser.add_argument('-d','--debug', action="store_true",help='Enables debug mode for Flask server')
  parser.add_argument('-t','--terminal', action="store_true",help='Starts in Terminal mode')
  args = vars(parser.parse_args())
  # print(args) # debug: check args

  if args['web']:
    if args['debug']:
      webFlask(True)
    else:
      webFlask(False)
  elif args['terminal']:
    terminalGUI()
  else:
    parser.print_help()

def webFlask(debug):
  ### Open browser
  url = 'http://127.0.0.1:5000/'
  webbrowser.open(url, new=2, autoraise=True)

  ### Setting up Flask server
  app.config['ENV'] = 'development'
  if debug:
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
  # print(app.config) # debug: server config
  url = '127.0.0.1'
  port = 5000
  app.run(url,port) # runs Flask server

def terminalGUI():
  print("Terminal GUI is a Work in progress.")


if __name__ == '__main__':
  main()
