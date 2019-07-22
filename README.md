# MineSweeper
Made by, Kiko Oliveira

This is a MineSweeper game, made using Python and Flask.
It was made for fun, its nothing amazing (expect bugs) and enjoy ^^

## Requirements

* Python3
  * Flask
  * npyscreen
    * curses

## Notes

I assume Python3 is already installed, as its not hard to do so, and probably already have installed out of the box.

I tried to make the install and run as easy as possible, using .bat files for Windows and a makefile for Linux.

Advices for improvements are appreciated!!!


## Linux

For Linux the game can be played either in a Web browser, or directly in the terminal.

### Install

Move to the folder `files`.
There you can run `make install` and this will install Flask.

### Runing

#### Runing Web

Move to the folder `files`.
There you can run `make web` in the bash and this will run the game server.

Runing will run the server and open a tab on your default browser on the page for the game (http://localhost:5000).

NOTE: If you are using Ubuntu Bash on Windows, it will not auto open the browser. I understand vaguely why this happens, but i haven't found a simple solution to fix it.
(Let me know if you know any easy fix. Thanks.)

#### Runing Terminal

Move to the folder `files`.
There you can run `make terminal` in the bash and this will run the game.

Runing will open a game menu directly in the Terminal.
The controls are very simple, using only arrows and enter, and a few shortcuts that are shown when needed.


## Windows

For windows only Web browser is available.

### Install

Open the folder `files` and then open the `install.bat`.
This will install Flask.

### Runing

#### Runing Web

Open the folder `files` and then open the `runWeb.bat`.

This will run the server and open a tab on your default browser on the page for the game (http://localhost:5000).
