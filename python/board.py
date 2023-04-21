from piece import Piece
class Board:
    """
    A class to represent a chess board

    Constructor takes in a FEN string to create a new board, with the
    default being the starting position FEN string
    Learn more about FEN here: https://www.chess.com/terms/fen-chess

    This class does not deal with any sort of logic other than parsing the 
    positional part of a FEN string. It does not validate moves or even parse
    algebraic notation, it solely has methods that allow indirect altering of
    the board's representation, with moves represented as previous 2D List 
    position, new 2D list position. These moves are parsed from algebraic 
    notation and validated in the Chess class, and then converted to that
    form and sent to this class to update the Board. 
    """

    def __init__(self, fen):
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
        self.pieces = Piece.init_pieces(self.board)

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
