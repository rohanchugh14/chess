# from PIL import Image
from tkinter import PhotoImage
import os

class Piece:
    """
    A class to represent a chess piece, with a color, row, and column
    Inherited by each individual piece class to override methods like
    move and generate_moves()
    """
    # very weird tkinter bug where I must keep a reference to the images
    # or else they will not show up due to garbage collection...    
    # class variables, images for all pieces, one dictionary for each color
    images = []
    DOT_IMAGE = None

    # parent class of all pieces
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

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


class Queen(Piece):
    # queen class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

class Rook(Piece):
    # rook class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

class Bishop(Piece):
    # bishop class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

class Knight(Piece):
    # knight class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

class Pawn(Piece):
    # pawn class
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
