from board import Board
from piece import Piece

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

    

    def select_piece(self, piece):
        """
        Selects a piece on the board and returns a list of possible moves.
        """
        self.selected_piece = piece
        moves = piece.generate_moves(self.board.piece_board)
        moves = piece.prune_moves(self.board, moves)
        return moves

   

    @staticmethod
    def __convert_pos(pos):
        """
        Takes a string position on the board e.g. "e4" and converts it to 
        row,col for use in the Board class.
        """
        col = pos[0] - 'a'
        row = 8 - pos[1] - 1
        return row, col

    def make_move(self, move):
        """
        Makes the move on the board according to whose turn it currently is.
        """
