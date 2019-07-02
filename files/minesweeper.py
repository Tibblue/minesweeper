#!/usr/bin/env python3
"""Minesweeper Game package

Can run the game in the browser using Flask.
Use --help to show the possible flags and their use

TODO: Make TerminalGUI
FIXME: Separate Web and Terminal stuff (after doing terminalGUI XD)
"""

from generator import *
import argparse
import webbrowser
from flask import *

minefield = None

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

  <title>Minesweeper</title>

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
    global minefield
    if minefield is None:
      # session['minefield'] = Minefield(20,10,30)
      minefield = Minefield(20,10,30)
    minefieldHTML = drawField()
    if request.args.get('assist') is not None:
      minefieldHTML += '<br>'+drawFieldOpen()
    else:
      minefieldHTML += '''
        <br>
        <button type="button">
          <a href="/?assist=yes">Show Minefield (use for guidance)</a>
        </button>
      '''
    return render_template('play.html', minefieldHTML=minefieldHTML)
    # return render_template('play.html', minefieldClass=minefield, minefieldHTML=minefieldHTML)

  @app.route('/victory')
  def victory():
    global minefield
    minefield = Minefield(20,10,30)
    html = f'<h1>You Won!!!</h1>'
    html += buttons
    return html

  @app.route('/lost')
  def lost():
    global minefield
    minefield = Minefield(20,10,30)
    html = f'<h1>You Lost</h1>'
    html += buttons
    return html

  @app.route('/leftClick')
  def leftClick():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    result = minefield.click(x,y,expand=True)
    if result==-1:
      return redirect(url_for('lost'))
    else:
      # if 'lastURL' in session:
      #   return redirect(session['lastURL'])
      return redirect(url_for('play'))

  @app.route('/rightClick')
  def rightClick():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    minefield.flag(x,y)
    if minefield.checkVictory():
      return redirect(url_for('victory'))
    else:
      return redirect(url_for('play'))

  @app.route('/newMapEasy')
  def newMapEasy():
    global minefield
    minefield = Minefield(10,8,10)
    return redirect(url_for('play'))

  @app.route('/newMapNormal')
  def newMapNormal():
    global minefield
    minefield = Minefield(20,10,30)
    return redirect(url_for('play'))

  @app.route('/newMapHard')
  def newMapHard():
    global minefield
    minefield = Minefield(30,20,125)
    return redirect(url_for('play'))

  @app.route('/custom')
  def newMapCustom():
    global minefield
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))
    nMines = int(request.args.get('nMines'))
    # In case there are too many mines, flashes a message to the user
    if nMines > width*height/2:
      flash('Too many Mines (cannot have more than half the field with mines)')
      return redirect(url_for('play'))
    minefield = Minefield(width,height,nMines)
    return redirect(url_for('play'))


### DRAW functions
def drawField():
  """Makes HTML for the minefield view"""

  global minefield
  matrix = minefield.matrixTuples

  html = f'<h1>{minefield.width}x{minefield.height} - {minefield.nMines} Minas</h1>'
  html += '<table oncontextmenu="return false;">'
  for y in range(minefield.height):
    html += '<tr>'
    for x in range(minefield.width):
      html += '<td align="center" width="32" height="32"'
      if matrix[y][x][0]==0:
        html += f' onmouseup="WhichButton(event,{x},{y})"><img src="/static/images/block.jpg" alt="Block" width="32" height="32">'
      elif matrix[y][x][0]==-1:
        html += f' onmouseup="WhichButton(event,{x},{y})"><img src="/static/images/flag.jpg" alt="Flag" width="32" height="32">'
      elif matrix[y][x][1]==-1:
        html += f'><img src="/static/images/mineRED.jpg" alt="Mine" width="32" height="32">'
      else:
        if matrix[y][x][1]>4:
          html += f' style="background-color:rgb(255, 64, 64)">'
        elif matrix[y][x][1]==4:
          html += f' style="background-color:rgb(255, 128, 32)">'
        elif matrix[y][x][1]==3:
          html += f' style="background-color:rgb(224, 224, 32)">'
        elif matrix[y][x][1]==2:
          html += f' style="background-color:rgb(64, 192, 64)">'
        elif matrix[y][x][1]==1:
          html += f' style="background-color:rgb(64, 192, 255)">'
        else:
          html += f' style="background-color:rgb(192, 192, 192)">'
        html += '<span style="font-size:20px">'+str(matrix[y][x][1])+'</span>'
      html += '</td>'
    html += '</tr>'
  html += '</table>\n'
  return html

def drawFieldOpen():
  """Makes HTML for the minefield view (all squares revealed/visible)"""

  global minefield
  matrix = minefield.matrixTuples

  html = f'<h3>{minefield.width}x{minefield.height} - {minefield.nMines} Minas</h3>'
  html += '<table>'
  for y in range(minefield.height):
    html += '<tr>'
    for x in range(minefield.width):
      html += '<td align="center" width="24" height="24"'
      if matrix[y][x][1]==-1:
        html += '><img src="/static/images/mineRED.jpg" alt="Mine" width="24" height="24">'
      else:
        if matrix[y][x][1]>4:
          html += ' style="background-color:rgb(255, 64, 64);">'
        elif matrix[y][x][1]==4:
          html += ' style="background-color:rgb(255, 128, 32);">'
        elif matrix[y][x][1]==3:
          html += ' style="background-color:rgb(224, 224, 32);">'
        elif matrix[y][x][1]==2:
          html += ' style="background-color:rgb(64, 192, 64);">'
        elif matrix[y][x][1]==1:
          html += ' style="background-color:rgb(64, 192, 255);">'
        else:
          html += ' style="background-color:rgb(192, 192, 192);">'
        html += '<span style="font-size:16">'+str(matrix[y][x][1])+'</span>'
      html += '</td>'
    html += '</tr>'
  html += '</table>\n'
  html += '<span>Mines Position: '+str(minefield.posMines)+'</span>' # debug
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
  app.secret_key = b'batatas'
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
