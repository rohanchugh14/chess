from tkinter import *
from tkinter import ttk
from board import Board


class Chess:
   """
   A class to represent a game of chess.
   This class focuses on handling aspects specific to the game, i.e. castling
   rights, whose turn it is, whether a player is in check, etc.

   It also parses player moves and validates whether or not they are legal,
   and then sends the valid moves to the Board class to update the board using
   simpler notation. 
   """


   def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
      self.board = Board(fen)
      self.white_turn = True

   def __str__(self):
      return str(self.board)
   
   def parse_move(self, move):
      pass

   def make_move(self, move):
      """
      Makes the move on the board according to whose turn it currently is.
      """


