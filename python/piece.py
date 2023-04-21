from PIL import Image
import os

class Piece:
    """
    A class to represent a chess piece, with a color, row, and column
    Inherited by each individual piece class to override methods like
    move and generate_moves()
    """
    # class variable, images for all pieces, one dictionary for each color
    images = []

    # parent class of all pieces
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    @staticmethod
    def init_pieces(fen_board):
        # load images
        Piece.load_images()
        # initialize all pieces in an array from a FEN string conversion
        # of a board
        pieces = []
        for row in range(len(fen_board)):
            for col in range(len(row)):
                square = fen_board[row][col]
                color = 0 if square.isupper() else 1
                square = square.lower()
                if square != ' ':
                    # match statement only in python 3.10
                    if square == 'k':
                        pieces.append(King(color, row, col))
                    elif square == 'q':
                        pieces.append(Queen(color, row, col))
                    elif square == 'r':
                        pieces.append(Rook(color, row, col))
                    elif square == 'b':
                        pieces.append(Bishop(color, row, col))
                    elif square == 'n':
                        pieces.append(Knight(color, row, col))
                    elif square == 'p':
                        pieces.append(Pawn(color, row, col))
        return pieces
    @staticmethod
    def load_images():
        # two dictionaries, one for each color
        # image[0] is white, image[1] is black
        
        images = []
        images.append({})
        images.append({})
        for filename in os.listdir('../img'):
            color, piece_name = filename[:-4].split('_')
            img = Image.open(f'../img/{filename}')

            if color == "white":
                images[0][piece_name] = img
            else:
                images[1][piece_name] = img


        return images
        # load images for each piece

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
