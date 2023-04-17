class Board:
   # a class to represent a chess board

   # constructor takes in a FEN string to create a new board, with the
   # default being the starting position FEN string
   # Learn more about FEN here: https://www.chess.com/terms/fen-chess
   def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
      """
      A constructor for a chess board that can take in a FEN string for a 
      starting position or use the default chess board to start. 
      """
      self.board = []
      fen = fen.split('/')
      for rank in fen:
         row = []
         for char in rank:
            # number - skip n files
            if char.isdigit():
               for i in range(int(char)):
                  row.append(' ')
            # piece - add to row
            else:
               row.append(char)
         self.board.append(row)
   
   def __str__(self):
      """
      Returns the string representation of the chess board at it's current 
      state. Lowercase represents black pieces and uppercase represents white.
      """
      board_str = ""
      # add top border
      for i in range(8):
         board_str += "+---"
      board_str += "+\n"
      # add each row with a border below
      for rank in self.board:
         for char in rank:
            board_str += "| " + char + " "
         board_str += "|\n"
         for i in range(8):
            board_str += "+---"
         board_str += "+\n"
      return board_str