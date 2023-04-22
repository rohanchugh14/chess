class Move:
    """
    A class to represent a move in chess.
    """

    # initialize the move
    def __init__(self, piece, new_pos):
        self.piece = piece
        self.new_pos = new_pos
    
    # set the image of the move
    def set_img(self, img):
        self.img = img

    # debug output for move
    def __repr__(self):
        return str(self)

    # string output for move
    def __str__(self):
        return f"{self.piece} to {self.new_pos}\n"