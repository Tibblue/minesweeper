#!/usr/bin/env python3
"""Minesweeper Game package (Terminal)

Runs the game in the Terminal using npyscreen.

TODO: maybe add flags to change the TUI before initializing
TODO: use flags to start game immediately at X dificulty
TODO: add ranking, and in-game timer
TODO: add ranking export and import (JSON/CSV)
"""

import npyscreen as nps
import regex as re
from generator import *

class App(nps.NPSAppManaged):
  """Minesweeper App Module

  This extends the class NPSAppManaged from npyscreen.
  It defines the Forms to be used later on start.
  It also define "menu" as the first Form.
  """

  STARTING_FORM = "menu"
  def onStart(self):
    self.addForm("menu", MenuForm, "Minesweeper - Main Menu", minimum_lines=16)
    self.addForm("custom", CustomMapForm, "Minesweeper - Custom Dificulty", minimum_lines=16)
    self.addForm("map", MapForm, "Minesweeper - Game", minimum_lines=28)

### FORMS
class MenuForm(nps.ActionForm):
  """Menu Form Module

  This extends the class ActionForm from npyscreen.

  It contains a Field for the Player Name and Dificulty selector.
  Pressing Cancel leaves the game.
  Pressing OK takes the Player to the game Screen/Form, unless the player
  selected the Custom dificulty (in this case player is taken to a extra
  Form, for custom size settings, before going into game).
  """

  def create(self):
    """Create Custom Form

    This function is called when Custom Form is created.
    It creates all the widgets for the Form.
    """

    # self.example = self.add(nps.TitleFixedText, name="Fixed Title", value="Fixed Label", editable=False, labelColor="STANDOUT", color="CAUTION")
    self.player = self.add(nps.TitleText, name="Name:", labelColor="STANDOUT")
    self.nextrely += 1
    self.dificulty = self.add(nps.TitleSelectOne, name="Dificulty", values=["Custom", "Easy", "Normal", "Hard"], value=[1], labelColor="STANDOUT", max_height=5, scroll_exit=True)
    self.nextrely += 1
    self.add(nps.FixedText, value="Maximazing the Terminal is very advised!", editable=False, color="CAUTION")

  def on_ok(self):
    map = self.parentApp.getForm("map")
    map.player.value = self.player.value
    selectedDificulty = self.dificulty.values[self.dificulty.value[0]]
    map.dificulty.value = selectedDificulty
    if selectedDificulty == "Custom":
      self.parentApp.setNextForm("custom")
    else:
      if selectedDificulty == "Easy":
        map.width.value = 10
        map.height.value = 8
        map.mines.value = 10
      elif selectedDificulty == "Normal":
        map.width.value = 20
        map.height.value = 10
        map.mines.value = 30
      elif selectedDificulty == "Hard":
        map.width.value = 30
        map.height.value = 20
        map.mines.value = 125
      map.gen_map(map.width.value,map.height.value,map.mines.value)
      self.parentApp.setNextForm("map")

  def on_cancel(self):
    self.parentApp.setNextForm(None)
    # self.parentApp.switchForm(None)

class CustomMapForm(nps.ActionForm):
  """Custom Form Module

  This extends the class ActionForm from npyscreen.

  It contains 3 sliders for the Player to choose the Custom Widht, Height and Number of Mines.
  Pressing Cancel takes the Player back to the Menu.
  Pressing OK takes the Player to the game Screen/Form.

  Note: Number of Mines cannot be greater than half of the Minefield size.
  """

  def create(self):
    """Create Custom Form

    This function is called when Custom Form is created.
    It creates all the widgets for the Form.
    """

    self.width = self.add(nps.TitleSlider, name="Custom Width (Min 5 | Max 40):", labelColor="STANDOUT", lowest=5, out_of=40, value=5)
    self.height = self.add(nps.TitleSlider, name="Custom Height (Min 5 | Max 20):", labelColor="STANDOUT", lowest=5, out_of=20, value=5)
    self.mines = self.add(nps.TitleSlider, name="Custom Number of Mines (Min 10 | Max W*H/2):", labelColor="STANDOUT", lowest=10, out_of=400, value=10)

  def on_ok(self):
    size = int(self.width.value)*int(self.height.value)
    if int(self.mines.value) > size/2 :
      nps.notify_confirm("Map cannot have more than half mine squares!!!\n(Number Mines > Half Map Size)", "Too many mines!!!", editw=1)
    else:
      map = self.parentApp.getForm("map")
      map.width.value = int(self.width.value)
      map.height.value = int(self.height.value)
      map.mines.value = int(self.mines.value)
      map.gen_map(map.width.value,map.height.value,map.mines.value)
      self.parentApp.setNextForm("map")

  def on_cancel(self):
    self.parentApp.switchFormPrevious()


class MapForm(nps.FormBaseNew):
  """Map Form Module

  This extends the class FormBaseNew from npyscreen.

  It contains information about the game (player name and minefield size and mine number) and the minefield.
  List of Shortcuts:
    -> d - discover/reveals a square
    -> f - flags a square
    -> q - quit/leave game
    -> r - restart game
    -> p - pause game (TODO)
    -> arrows - move cursor
    -> h/j/k/l - move cursor

  Attributes
  ----------
  minefieldClass : Minefield Class from generator.py
    Matrix where each position is a Tuple (Status,Number)

  NOTES:
    Each cell/square (from the class matrixTuples variable) is a
    Tuple (Status,Number)
      -> status - (flaged -1/hidden 0/visible 1)
      -> number - square number (or -1 for mines)
  """

  def h_flag(self, ascii_code):
    """Minefield Flag handler

    This function handles a right-click.
    This flags a square in-game.
    """

    x = self.minefieldGrid.edit_cell[1]
    y = self.minefieldGrid.edit_cell[0]
    self.minefieldClass.flag(x,y)
    if self.minefieldClass.checkVictory():
      response = nps.notify_yes_no("You Won the Game !!!\nDo you wish to replay the Map?", title="VICTORY", form_color='STANDOUT', wrap=True, editw=1)
      if response:
        self.gen_map(int(self.width.value),int(self.height.value),int(self.mines.value))
        self.display()
      else:
        self.parentApp.switchForm("menu")

  def h_discover(self, ascii_code):
    """Minefield Click handler

    This function handles a left-click.
    This reveals a square in-game.
    """

    x = self.minefieldGrid.edit_cell[1]
    y = self.minefieldGrid.edit_cell[0]
    result = self.minefieldClass.click(x,y,expand=True)
    if result == -2: # mine on first square
      while result == -2: # generate new map until its safe
        self.gen_map(int(self.width.value),int(self.height.value),int(self.mines.value))
        result = self.minefieldClass.click(x,y,expand=True)
      self.display()
    if result == -1: # mine
      response = nps.notify_yes_no("You Lost the Game :(\nDo you wish to retry the Map?", title="LOST", form_color='STANDOUT', wrap=True, editw=1)
      if response:
        self.gen_map(int(self.width.value),int(self.height.value),int(self.mines.value))
        self.display()
      else:
        self.parentApp.switchForm("menu")

  def h_terminate(self, ascii_code):
    """Minefield Terminate handler

    This terminates/quits the current game, returning to the Menu.
    """

    self.parentApp.switchForm("menu")

  def h_restart(self, ascii_code):
    """Minefield Restart handler

    This restarts the game, with a new Minefield, but the same settings.
    """

    self.gen_map(int(self.width.value),int(self.height.value),int(self.mines.value))

  def create(self):
    """Create Map Form

    This function is called when Map Form is created.
    It creates all the widgets for the Form and the shortcut handlers.
    """

    new_handlers = {
      "d" : self.h_discover,
      "f" : self.h_flag,
      "t" : self.h_terminate,
      "r" : self.h_restart,
      # "p" : self.h_pause,
    }
    self.add_handlers(new_handlers)

    # INFO area
    self.player = self.add(nps.TitleFixedText, name="Your Name: ", labelColor="STANDOUT", use_two_lines=False, begin_entry_at=11, editable=False)
    self.dificulty = self.add(nps.TitleFixedText, name="Dificulty: ", labelColor="STANDOUT", use_two_lines=False, begin_entry_at=11, editable=False)
    self.nextrelx += 24
    self.nextrely -= 1
    self.width = self.add(nps.TitleFixedText, name="Width: ", labelColor="STANDOUT", use_two_lines=False, begin_entry_at=7, editable=False)
    self.nextrelx += 16
    self.nextrely -= 1
    self.height = self.add(nps.TitleFixedText, name="Height: ", labelColor="STANDOUT", use_two_lines=False, begin_entry_at=8, editable=False)
    self.nextrelx += 16
    self.nextrely -= 1
    self.mines = self.add(nps.TitleFixedText, name="Mines: ", labelColor="STANDOUT", use_two_lines=False, begin_entry_at=7, editable=False)

    # SHORTCUTS area
    self.nextrelx = 2
    self.add(nps.FixedText, value="Shorcuts: ", color="STANDOUT", editable=False)
    self.nextrelx += 12
    self.nextrely -= 1
    self.add(nps.TitleFixedText, name="d: ", value="click", labelColor="GOOD", use_two_lines=False, begin_entry_at=4, editable=False)
    self.add(nps.TitleFixedText, name="f: ", value="flag", labelColor="GOOD", use_two_lines=False, begin_entry_at=4, editable=False)
    self.add(nps.TitleFixedText, name="t: ", value="terminate", labelColor="GOOD", use_two_lines=False, begin_entry_at=4, editable=False)
    self.add(nps.TitleFixedText, name="r: ", value="restart", labelColor="GOOD", use_two_lines=False, begin_entry_at=4, editable=False)
    # self.add(nps.TitleFixedText, name="p: ", value="pause", labelColor="GOOD", use_two_lines=False, begin_entry_at=4, editable=False)

    # MINEFIELD area
    self.nextrelx = 2
    self.nextrely += 1
    self.minefieldGrid = self.add(MinefieldGridWidget, name=" ", column_width=2, col_margin=0, row_height=1)

  def gen_map(self, width, height, mines):
    """Generate Minesweeper Map

    Uses the Minefield Class from generator.py
    Creates a instance of Minefield with the given paramaters and
    passes the matrix values to the Minefield widget values.
    """

    self.minefieldClass = Minefield(width,height,mines)
    self.minefieldGrid.values = self.minefieldClass.matrixTuples


### WIDGETS
class MinefieldGridWidget(nps.SimpleGrid):
  """Minefield Widget Module

  This extends the class SimpleGrid from npyscreen.

  It contains the minefield grid.
  It applies custom colors to the square depending on the square value.

  NOTES:
    Each cell is a Tuple (Status,Number)
      -> status - (flaged -1/hidden 0/visible 1)
      -> number - square number (or -1 for mines)
  """

  def custom_print_cell(self, actual_cell, display_value):
    """Custom cell color and value

    This function changes the color of the cell, depending on its
    gameplay status and value.
    """

    if display_value:
      aux = re.sub("[()]","",display_value)
      aux = re.split(", ", aux)
      status = aux[0]
      number = aux[1]
      square = tuple((status,number))
      if status == "-1":
        actual_cell.value = "F"
        actual_cell.color = 'CAUTION'
      elif status == "0":
        actual_cell.value = "#"
        actual_cell.color = 'DEFAULT' # debug
        # actual_cell.color = 'VERYGOOD' # debug
      else:
        if number == "-1":
          actual_cell.value = "*"
          actual_cell.color = 'CAUTION' # debug
          # actual_cell.color = 'CRITICAL' # debug
        else:
          actual_cell.value = number
          if number == "0":
            actual_cell.value = " "
            actual_cell.color = 'DEFAULT'
          elif number == "1":
            actual_cell.color = 'STANDOUT'
          elif number == "2":
            actual_cell.color = 'SAFE'
          elif number == "3":
              actual_cell.color = 'DANGER'
          elif number == "4":
              actual_cell.color = 'NO_EDIT'
          elif number == "5":
              actual_cell.color = 'NO_EDIT'
          elif number == "6":
              actual_cell.color = 'NO_EDIT'
          elif number == "7":
              actual_cell.color = 'NO_EDIT'
          elif number == "8":
              actual_cell.color = 'NO_EDIT'
          # else:
          #   actual_cell.color = 'DEFAULT' # debug



def runTerminal():
  """Run the game in Terminal"""

  app = App()
  app.run()

if __name__ == "__main__":
  runTerminal()
