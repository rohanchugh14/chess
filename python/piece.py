from move import Move
from tkinter import PhotoImage
import os

class Piece:
    """
    A class to represent a chess piece, with a color, row, and column
    Inherited by each individual piece class to override methods like
    generate_moves()

    generate_moves() will only generate pseudo-legal moves, and will not
    check for any sort of self-check. The Piece class will have a method
    to prune any moves that would result in self-check to generate the
    true legal moves for a piece.
    """
    # very weird tkinter bug where I must keep a reference to the images
    # or else they will not show up due to garbage collection...    
    # class variables, images for all pieces, one dictionary for each color
    images = []
    DOT_IMAGE = None

    # references for each king to deal with checks and legality of moves
    BLACK_KING = None
    WHITE_KING = None

    # parent class of all pieces
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    # string representation of piece
    def __str__(self):
        color = "White" if self.color == 0 else "Black"
        return f"{color} {self.__class__.__name__} at ({self.row}, {self.col})"

    def __repr__(self):
        return str(self)
    # generate moves, overriden by each piece
    def generate_moves(self, board):
        pass

    # prune moves that would result in self-check
    def prune_moves(self, board, moves):
        
        updated_moves = []
        for i in range(len(moves)):
            move = moves[i]
            # make the move
            captured_piece, old_row, old_col = board.make_move(move)
            # check if the king is in check
            if not board.is_in_check(self.color):
                updated_moves.append(move)
            # undo the move
            board.undo_move(move, captured_piece, old_row, old_col)
        
        return updated_moves
    # set image for piece
    def set_img(self, img):
        self.img = img
    
    # get image for piece
    def get_img(self):
        return self.img
    # initialize self.pieces array for Board class
    @staticmethod
    def init_pieces(fen_board):
        # load images
        Piece.load_images()
        # initialize all pieces in an array from a FEN string conversion
        # of a board
        piece_board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(None)
            piece_board.append(row)
        
        pieces = []
        for row in range(len(fen_board)):
            for col in range(len(fen_board[0])):
                square = fen_board[row][col]
                color = 0 if square.isupper() else 1
                square = square.lower()
                if square != ' ':
                    # match statement only in python 3.10
                    if square == 'k':
                        piece = King(color, row, col)
                        pieces.append(piece)
                        piece_board[row][col] = piece
                    elif square == 'q':
                        piece = Queen(color, row, col)
                        # print(piece.generate_moves(fen_board))
                        pieces.append(piece)
                        piece_board[row][col] = piece
                    elif square == 'r':
                        piece = Rook(color, row, col)
                        pieces.append(piece)
                        piece_board[row][col] = piece
                    elif square == 'b':
                        piece = Bishop(color, row, col)
                        pieces.append(piece)
                        piece_board[row][col] = piece
                    elif square == 'n':
                        piece = Knight(color, row, col)
                        pieces.append(piece)
                        piece_board[row][col] = piece
                    elif square == 'p':
                        piece = Pawn(color, row, col)
                        pieces.append(piece)
                        piece_board[row][col] = piece
        return pieces, piece_board
    # load images for each piece
    @staticmethod
    def load_images():
        # two dictionaries, one for each color
        # image[0] is white, image[1] is black
        
        images = []
        images.append({})
        images.append({})
        for filename in os.listdir('../img/pieces'):
            color, piece_name = filename[:-4].split('_')
            img = PhotoImage(file=f'../img/pieces/{filename}')
            piece_ltr = piece_name[0] if piece_name != 'knight' else 'n'
            if color == "white":
                images[0][piece_ltr] = img
            else:
                images[1][piece_ltr] = img
        
        Piece.images = images
        Piece.DOT_IMAGE = PhotoImage(file='../img/target.png')
        

class King(Piece):
    # king class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        if color == 0:
            Piece.WHITE_KING = self
        else:
            Piece.BLACK_KING = self
    
    # generate moves for king
    def generate_moves(self, board):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                # want to skip (0,0) offset
                if i == 0 and j == 0:
                    continue
                # check if square is in bounds
                if self.row + i < 0 or self.row + i >= 8 or self.col + j < 0 \
                      or self.col + j >= 8:
                    continue
                # if the square is empty, add it as a legal move
                if board[self.row + i][self.col + j] is None :
                    moves.append(Move(self, (self.row + i, self.col + j)))
                # if the square is occupied by an enemy piece, add it as a 
                # legal move
                elif board[self.row + i][self.col + j].color != self.color:
                    moves.append(Move(self, (self.row + i, self.col + j)))
        return moves


class Queen(Piece):
    # queen class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        if color == 0:
            Piece.WHITE_QUEEN = self
        else:
            Piece.BLACK_QUEEN = self
    
    # generate moves for queen
    def generate_moves(self, board):
        moves = []
        # generate moves for rook
        tempRook = Rook(self.color, self.row, self.col)
        moves += tempRook.generate_moves(board)
        # generate moves for bishop
        tempBishop = Bishop(self.color, self.row, self.col)
        moves += tempBishop.generate_moves(board)
        for move in moves:
            move.piece = self
        return moves

class Rook(Piece):
    # rook class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
    
    # generate moves for rook
    def generate_moves(self, board):
        moves = []
        # loop through rook offsets
        for x_offset, y_offset in [(0,1),(0,-1),(1,0),(-1,0)]:
            x, y = self.row + x_offset, self.col + y_offset
            # loop through all squares in that direction
            while 0 <= x < 8 and 0 <= y < 8:
                # if square is empty, add it as a legal move
                if board[x][y] is None:
                    moves.append(Move(self, (x,y)))
                # if square is our piece, stop searching in that direction
                elif board[x][y].color == self.color:
                    break
                # square is enemy piece, add to moves and stop searching in 
                # that direction
                else:
                    moves.append(Move(self, (x,y)))
                    break
                x += x_offset
                y += y_offset
        return moves

class Bishop(Piece):
    # bishop class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    # generate moves for bishop
    def generate_moves(self, board):
        moves = []
        # loop through bishop offsets
        for x_offset, y_offset in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            x, y = self.row + x_offset, self.col + y_offset
            # loop through all squares in that direction
            while 0 <= x < 8 and 0 <= y < 8:
                # if square is empty, add it as a legal move
                if board[x][y] is None:
                    moves.append(Move(self, (x,y)))
                # if square is our piece, stop searching in that direction
                elif board[x][y].color == self.color:
                    break
                # square is enemy piece, add to moves and stop searching in 
                # that direction
                else:
                    moves.append(Move(self, (x,y)))
                    break
                x += x_offset
                y += y_offset
        return moves

class Knight(Piece):
    # knight class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    # generate moves for knight
    def generate_moves(self, board):
        moves = []
        # loop through knight offsets
        for x_offset, y_offset in [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),\
                                   (-2,1),(-2,-1)]:
            x, y = self.row + x_offset, self.col + y_offset
            # if square is in bounds
            if 0 <= x < 8 and 0 <= y < 8:
                # if square is empty, add it as a legal move
                if board[x][y] is None:
                    moves.append(Move(self, (x,y)))
                # if square is our piece, skip
                elif board[x][y].color == self.color:
                    pass
                # square is enemy piece, add to moves
                else:
                    moves.append(Move(self, (x,y)))
        return moves

class Pawn(Piece):
    # pawn class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
    
    # generate moves for pawn
    def generate_moves(self, board):
        moves = []
        # if pawn is white
        if self.color == 0:
            # if pawn is on starting row
                # if square in front of pawn is empty
            if board[self.row - 1][self.col] is None:
                moves.append(Move(self,(self.row - 1, self.col)))
                # if square 2 in front of pawn is empty and it's on the 
                # starting row
                if self.row == 6 and board[self.row - 2][self.col] is None:
                    moves.append(Move(self,(self.row - 2, self.col)))
           
            # if pawn can capture to the top right
            if self.col < 7 and self.row > 0 and \
                board[self.row - 1][self.col + 1] is not None and \
                    board[self.row - 1][self.col + 1].color != self.color:
                moves.append(Move(self,(self.row - 1, self.col + 1)))
            # if pawn can capture to top left
            if self.col > 0 and self.row > 0 and \
                board[self.row - 1][self.col - 1] is not None and \
                    board[self.row - 1][self.col - 1].color != self.color:
                moves.append(Move(self,(self.row - 1, self.col - 1)))
        # if pawn is black
        else:
            # if pawn is on starting row
            # if square in front of pawn is empty
            if board[self.row + 1][self.col] is None:
                moves.append(Move(self,(self.row + 1, self.col)))
                # if square 2 in front of pawn is empty and it's on the 
                # starting row
                if self.row == 1 and board[self.row + 2][self.col] is None:
                    moves.append(Move(self, (self.row + 2, self.col)))
           
            # if pawn can capture to the right
            if self.col < 7 and self.row < 7 and \
                board[self.row + 1][self.col + 1] is not None and \
                    board[self.row + 1][self.col + 1].color != self.color:
                moves.append(Move(self, (self.row + 1, self.col + 1)))
            # if pawn can capture to left
            if self.col > 0 and self.row < 7 and \
                board[self.row + 1][self.col - 1] is not None and \
                    board[self.row + 1][self.col - 1].color != self.color:
                moves.append(Move(self, (self.row + 1, self.col - 1)))
        return moves
