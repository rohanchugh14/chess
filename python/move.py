class Move:
    def __init__(self, piece, new_pos):
        self.piece = piece
        self.new_pos = new_pos
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.piece} to {self.new_pos}\n"