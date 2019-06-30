#!/usr/bin/env python3
"""Minesweeper Game package

Can run the game in the browser using Flask.
Use --help to show the possible flags and their use

TODO: Make TerminalGUI
FIXME: Separate Web and Terminal stuff
"""

from generator import *
import argparse
import webbrowser
from math import trunc
from flask import *

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

def setRoutes(app):
  """Generates app Routes"""

  @app.route('/')
  def play():
    global matrixTup, posMines
    if matrixTup == []:
      return redirect(url_for('newMapNormal'))
    largura = matrixWidth(matrixTup)
    altura = matrixHeight(matrixTup)
    nMines = len(posMines)
    html = f'<h1>{largura}x{altura} - {nMines} Minas</h1>'
    html += buttons
    html += drawField()
    html += '<br><br><br><br><br>'
    html += drawFieldOpen()
    return html

  @app.route('/victory')
  def victory():
    global matrixTup, posMines
    minefield = newMinefield(20,10,30)
    matrixTup = minefield[0]
    posMines = minefield[1]
    html = f'<h1>You Won!!!</h1>'
    html += buttons
    return html

  @app.route('/lost')
  def lost():
    global matrixTup, posMines
    minefield = newMinefield(20,10,30)
    matrixTup = minefield[0]
    posMines = minefield[1]
    html = f'<h1>You Lost</h1>'
    html += buttons
    return html

  @app.route('/leftClick')
  def leftClick():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    result = click(x,y,matrixTup)
    if result==-1:
      return redirect(url_for('lost'))
    elif result==0:
      # TODO: expand surroundings
      return redirect(url_for('play'))
    elif result==1:
      return redirect(url_for('play'))
    elif result==2:
      return redirect(url_for('victory'))

  @app.route('/rightClick')
  def rightClick():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    flag(x,y,matrixTup)
    if checkVictory(matrixTup,posMines):
      return redirect(url_for('victory'))
    else:
      return redirect(url_for('play'))

  @app.route('/newMapEasy')
  def newMapEasy():
    global matrixTup, posMines
    minefield = newMinefield(10,8,10)
    matrixTup = minefield[0]
    posMines = minefield[1]
    return redirect(url_for('play'))

  @app.route('/newMapNormal')
  def newMapNormal():
    global matrixTup, posMines
    minefield = newMinefield(20,10,30)
    matrixTup = minefield[0]
    posMines = minefield[1]
    return redirect(url_for('play'))

  @app.route('/newMapHard')
  def newMapHard():
    global matrixTup, posMines
    minefield = newMinefield(30,20,125)
    matrixTup = minefield[0]
    posMines = minefield[1]
    return redirect(url_for('play'))

  @app.route('/custom')
  def newMapCustom():
    largura = int(request.args.get('largura'))
    altura = int(request.args.get('altura'))
    nMines = int(request.args.get('nMines'))
    minefield = newMinefield(largura,altura,nMines)
    matrixTup = minefield[0]
    posMines = minefield[1]
    return redirect(url_for('play'))


### DRAW functions
def drawField():
  """Makes HTML for the minefield view"""

  global matrixTup, posMines
  # for j in range(len(matrixTup)): # debug matrixTup print
  #   print(matrixTup[j]) # debug matrixTup print

  html = '<table oncontextmenu="return false;">\n'
  for y in range(matrixHeight(matrixTup)):
    html += '<tr>'
    for x in range(matrixWidth(matrixTup)):
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

def drawFieldOpen():
  """Makes HTML for the minefield view (all squares revealed/visible)"""

  global matrixTup, posMines
  # for j in range(len(matrixTup)): # debug matrixTup print
  #   print(matrixTup[j]) # debug matrixTup print

  html = '<table>\n'
  for y in range(matrixHeight(matrixTup)):
    html += '<tr>'
    for x in range(matrixWidth(matrixTup)):
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
  """Starts the game in the browser

  Automatically opens a new tab, on your default browser, with the game.
  Allows debug mode, in case you need it.
  """

  ## Define address and port
  address = '127.0.0.1'
  port = 5000

  ### Setting up Flask server
  app = Flask("Minesweeper")
  setRoutes(app)

  ### Open browser
  url = 'http://'+address+':'+str(port)+'/'
  webbrowser.open(url, new=2, autoraise=True)

  ### Starting server
  app.config['ENV'] = 'development'
  if debug:
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
  # print(app.config) # debug: server config

  app.run(address,port) # runs Flask server

def terminalGUI():
  """Starts the game in the terminal

  TODO: all of it
  """

  print("Terminal GUI is a Work in progress.")


if __name__ == '__main__':
  main()
