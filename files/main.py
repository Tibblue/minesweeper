#!/usr/bin/env python3
"""Minesweeper Game package

  Can run the game in the Browser using Flask.
  Can run the game in the Terminal using npyscreen.
  Use --help to show the possible flags and their use.

  Note: This is JUST a main calling all the other files. If you want
        one specific version, you are free to start Minesweeper directly
        from the specific file.

  TODO: Finish TerminalUI (TUI)
  TODO: Improve WebFlask (WebGUI)
"""

from webGUI import runWebFlask
from terminalUI import runTerminal
from argparse import ArgumentParser


def main():
  ### Parse Arguments
  parser = ArgumentParser()
  parser.add_argument('-w','--web', action="store_true",help='Starts in Web/Browser mode (Flask server)')
  parser.add_argument('-d','--debug', action="store_true",help='Enables debug mode for Flask server')
  parser.add_argument('-t','--terminal', action="store_true",help='Starts in Terminal mode')
  args = vars(parser.parse_args())
  # print(args) # debug: check args

  if args['web']:
    if args['debug']:
      runWebFlask(debug=True)
    else:
      runWebFlask(debug=False)
  elif args['terminal']:
    runTerminal(options=None)
  else:
    parser.print_help()


if __name__ == '__main__':
  main()
