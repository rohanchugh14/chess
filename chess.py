from tkinter import *
from tkinter import ttk
from board import Board


class Chess:


   def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
      self.board = Board(fen)
      self.white_turn = True

   def __str__(self):
      return str(self.board)
   
   def make_move(self, move):
      """
      Makes the move on the board according to whose turn it currently is.
      """


