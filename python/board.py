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

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
        """
        A constructor for a chess board that can take in a FEN string for a 
        starting position or use the default chess board to start. 
        """
        self.board = []
        self.selected_piece = None
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
        self.pieces, self.piece_board = Piece.init_pieces(self.board)
                
    def select_piece(self, piece):
        """
        Selects a piece on the board and returns a list of possible moves.
        """
        self.selected_piece = piece
        moves = piece.generate_moves(self.piece_board)
        moves = piece.prune_moves(self, moves)
        return moves

    def is_in_check(self, color):
        """
        Returns whether or not the given color is in check.
        """
        king = Piece.WHITE_KING if color == 0 else Piece.BLACK_KING
        # for each piece, check if it can move to the king's position
        for piece in self.pieces:
            if piece.color != color:
                moves = piece.generate_moves(self.piece_board)
                for move in moves:
                    if move.new_pos == (king.row, king.col):
                        return True
        return False
        pass

    def temp_move(self, move):
        """
        Takes in a move and makes it without updating tkinter board.
        Returns whatever was on the new position or None if empty to be 
        used again to undo the move.
        """
        old_row, old_col = move.piece.row, move.piece.col
        self.piece_board[old_row][old_col] = None
        piece_captured = self.piece_board[move.new_pos[0]][move.new_pos[1]]
        if piece_captured is not None:
            self.pieces.remove(piece_captured)
        self.piece_board[move.new_pos[0]][move.new_pos[1]] = move.piece
        move.piece.row, move.piece.col = move.new_pos[0], move.new_pos[1]
        return piece_captured, old_row, old_col

    def undo_move(self, move, piece_captured, old_row, old_col):
        """
        Takes in a move and undoes it without updating tkinter board.
        """
        # old_row, old_col = move.piece.row, move.piece.col
        self.piece_board[old_row][old_col] = move.piece
        self.piece_board[move.new_pos[0]][move.new_pos[1]] = piece_captured
        if piece_captured is not None:
            self.pieces.append(piece_captured)
        move.piece.row, move.piece.col = old_row, old_col

    def get_piece_str(self, row, col):
        """
        Returns the piece at the given row and column of the board.
        """
        return self.board[row][col]

    def get_piece(self, row, col):
        """
        Returns the piece at the given row and column of the board.
        """
        return self.piece_board[row][col]
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
