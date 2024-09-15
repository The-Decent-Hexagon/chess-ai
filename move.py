import piece


class Move:
    def __init__(self, board, start_square, end_square, promotion=None, enpassant=0, castle=False):
        self.board = board
        self.start_square = start_square
        self.end_square = end_square
        self.start_piece = self.board.grid[self.start_square]
        self.end_piece = self.board.grid[self.end_square]
        self.start_timesmoved = board.timesmoved[self.start_square]
        self.end_timesmoved = board.timesmoved[self.end_square]
        self.last_pawndoublepush = self.board.pawndoublepush
        self.promotion = promotion
        if(promotion==None):
            self.promotion = self.start_piece
        self.enpassant = enpassant
        self.castle = castle

    def __eq__(self, other):
        return self.board==other.board and self.start_square == other.start_square and self.end_square == other.end_square and self.promotion == other.promotion

    def __repr__(self):
        s = ""
        start = chr(97+self.start_square%8) + str(self.start_square//8+1)
        end = chr(97+self.end_square%8) + str(self.end_square//8+1)
        p = ""
        if self.promotion != self.start_piece:
            t = piece.gettype(self.promotion)
            if(t == piece.QUEEN):
                p = "q"
            elif(t == piece.BISHOP):
                p = "b"
            elif(t == piece.ROOK):
                p = "r"
            elif(t == piece.KNIGHT):
                p = "n"
        return start + end + p