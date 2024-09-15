#a1 is square 0
import random

import piece
import move

KNIGHTTABLE = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50,
]

QUEENTABLE = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]

BISHOPTABLE = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20,
]

PAWNTABLEBLACK = [
 0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0
]

PAWNTABLEWHITE = [
0,  0,  0,  0,  0,  0,  0,  0,
5, 10, 10, -20, -20, 10, 10, 5,
5, -5,-10,  0,  0,-10, -5,  5,
0,  0,  0, 20, 20,  0,  0,  0,
5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
0,  0,  0,  0,  0,  0,  0,  0
]

class Board:
    def __init__(self):
        self.grid = []
        self.timesmoved = []
        for _ in range(64):
            self.grid.append(0)
            self.timesmoved.append(0)
        #needed for en passant
        self.pawndoublepush = None
        self.turn = piece.WHITE

    def __eq__(self, other):
        return self.grid == other.grid and self.pawndoublepush == other.pawndoublepush and self.turn == other.turn

    def startingposition(self):
        self.grid[0] = piece.makepiece(piece.WHITE, piece.ROOK)
        self.grid[1] = piece.makepiece(piece.WHITE, piece.KNIGHT)
        self.grid[2] = piece.makepiece(piece.WHITE, piece.BISHOP)
        self.grid[3] = piece.makepiece(piece.WHITE, piece.QUEEN)
        self.grid[4] = piece.makepiece(piece.WHITE, piece.KING)
        self.grid[5] = piece.makepiece(piece.WHITE, piece.BISHOP)
        self.grid[6] = piece.makepiece(piece.WHITE, piece.KNIGHT)
        self.grid[7] = piece.makepiece(piece.WHITE, piece.ROOK)

        self.grid[56] = piece.makepiece(piece.BLACK, piece.ROOK)
        self.grid[57] = piece.makepiece(piece.BLACK, piece.KNIGHT)
        self.grid[58] = piece.makepiece(piece.BLACK, piece.BISHOP)
        self.grid[59] = piece.makepiece(piece.BLACK, piece.QUEEN)
        self.grid[60] = piece.makepiece(piece.BLACK, piece.KING)
        self.grid[61] = piece.makepiece(piece.BLACK, piece.BISHOP)
        self.grid[62] = piece.makepiece(piece.BLACK, piece.KNIGHT)
        self.grid[63] = piece.makepiece(piece.BLACK, piece.ROOK)

        for i in range(8,16):
            self.grid[i] = piece.makepiece(piece.WHITE, piece.PAWN)
        for i in range(48,56):
            self.grid[i] = piece.makepiece(piece.BLACK, piece.PAWN)

    def update_lists(self):
        self.pieces = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for i in range(len(self.grid)):
            self.pieces[self.grid[i]].append(i)

    def make_move(self, m):
        self.grid[m.start_square] = 0
        self.grid[m.end_square] = m.promotion
        self.timesmoved[m.start_square] = 0
        self.timesmoved[m.end_square] = m.start_timesmoved + 1
        #double pawn push
        if(self.turn == piece.WHITE):
            if(piece.gettype(m.start_piece)==piece.PAWN and m.start_square//8 == 1 and m.end_square//8 == 3):
                self.pawndoublepush = m.end_square
            else:
                self.pawndoublepush = 0
        else:
            if(piece.gettype(m.start_piece)==piece.PAWN and m.start_square//8 == 6 and m.end_square//8 == 4):
                self.pawndoublepush = m.end_square
            else:
                self.pawndoublepush = 0
        #en passant
        if(m.enpassant!=0):
            self.grid[m.enpassant]=0
        #castle
        if(m.castle):
            if(m.end_square==6):
                self.grid[5] = self.grid[7]
                self.grid[7] = 0
            elif(m.end_square==2):
                self.grid[3] = self.grid[0]
                self.grid[0] = 0
            if(m.end_square==62):
                self.grid[61] = self.grid[63]
                self.grid[63] = 0
            elif(m.end_square==58):
                self.grid[59] = self.grid[56]
                self.grid[56] = 0
        self.turn = piece.BLACK if self.turn == piece.WHITE else piece.WHITE
        self.update_lists()

    def unmake_move(self, m):
        self.grid[m.start_square] = m.start_piece
        self.grid[m.end_square] = m.end_piece
        self.timesmoved[m.start_square] = m.start_timesmoved
        self.timesmoved[m.end_square] = m.end_timesmoved
        self.pawndoublepush = m.last_pawndoublepush
        # en passant
        if (m.enpassant != 0):
            self.grid[m.enpassant] = piece.makepiece(self.turn, piece.PAWN)
        #castle
        if(m.castle):
            if(m.end_square==6):
                self.grid[7] = self.grid[5]
                self.grid[5] = 0
            elif(m.end_square==2):
                self.grid[0] = self.grid[3]
                self.grid[3] = 0
            elif(m.end_square==62):
                self.grid[63] = self.grid[61]
                self.grid[61] = 0
            elif(m.end_square==58):
                self.grid[56] = self.grid[59]
                self.grid[59] = 0
        self.turn = piece.BLACK if self.turn == piece.WHITE else piece.WHITE
        self.update_lists()

    def getpieces(self, p):
        l = []
        for i in range(64):
            if(self.grid[i] == p):
                l.append(i)

        return l

    def test(self, rank, file):
        if (rank < 0 or rank > 7):
            return False
        if (file < 0 or file > 7):
            return False
        if(self.grid[8*rank+file]!=0 and piece.getcolour(self.grid[8*rank+file]) == self.turn):
            return False
        return True

    def generate_pseudolegal_moves(self):
        moves = []
        #knights
        knights = self.pieces[piece.makepiece(self.turn, piece.KNIGHT)]
        for k in knights:
            rank = k//8
            file = k%8
            if(self.test(rank+2, file+1)): moves.append(move.Move(self, k, 8*(rank+2)+file+1))
            if(self.test(rank+2, file-1)): moves.append(move.Move(self, k, 8*(rank+2)+file-1))
            if(self.test(rank+1, file+2)): moves.append(move.Move(self, k, 8*(rank+1)+file+2))
            if(self.test(rank+1, file-2)): moves.append(move.Move(self, k, 8*(rank+1)+file-2))
            if(self.test(rank-1, file+2)): moves.append(move.Move(self, k, 8*(rank-1)+file+2))
            if(self.test(rank-1, file-2)): moves.append(move.Move(self, k, 8*(rank-1)+file-2))
            if(self.test(rank-2, file+1)): moves.append(move.Move(self, k, 8*(rank-2)+file+1))
            if(self.test(rank-2, file-1)): moves.append(move.Move(self, k, 8*(rank-2)+file-1))

        #bishops and queens
        bishops = self.pieces[piece.makepiece(self.turn, piece.BISHOP)]
        queens = self.pieces[piece.makepiece(self.turn, piece.QUEEN)]
        bishops.extend(queens)
        for b in bishops:
            #ur
            rank = b // 8
            file = b % 8
            while rank<7 and file<7:
                rank += 1
                file += 1
                if(self.grid[8*rank+file]!=0):
                    if(piece.getcolour(self.grid[8*rank+file])==self.turn):
                        break
                    else:
                        moves.append(move.Move(self, b, 8*rank+file))
                        break
                else:
                    moves.append(move.Move(self, b, 8*rank+file))

            #ul
            rank = b // 8
            file = b % 8
            while rank > 0 and file < 7:
                rank -= 1
                file += 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, b, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, b, 8 * rank + file))

            #dr
            rank = b // 8
            file = b % 8
            while rank < 7 and file > 0:
                rank += 1
                file -= 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, b, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, b, 8 * rank + file))

            #dl
            rank = b // 8
            file = b % 8
            while rank > 0 and file > 0:
                rank -= 1
                file -= 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, b, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, b, 8 * rank + file))

        #rooks and queens
        rooks = self.pieces[piece.makepiece(self.turn, piece.ROOK)]
        rooks.extend(queens)
        for r in rooks:
            # l
            rank = r // 8
            file = r % 8
            while rank > 0:
                rank -= 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, r, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, r, 8 * rank + file))

            # r
            rank = r // 8
            file = r % 8
            while rank < 7:
                rank += 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, r, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, r, 8 * rank + file))

            # u
            rank = r // 8
            file = r % 8
            while file < 7:
                file += 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, r, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, r, 8 * rank + file))

            # d
            rank = r // 8
            file = r % 8
            while file > 0:
                file -= 1
                if (self.grid[8 * rank + file] != 0):
                    if (piece.getcolour(self.grid[8 * rank + file]) == self.turn):
                        break
                    else:
                        moves.append(move.Move(self, r, 8 * rank + file))
                        break
                else:
                    moves.append(move.Move(self, r, 8 * rank + file))

        #pawns
        pawns = self.pieces[piece.makepiece(self.turn, piece.PAWN)]
        if(self.turn == piece.WHITE):
            for p in pawns:
                rank = p//8
                file = p%8
                #pushing forward
                if(self.grid[8*rank+8+file]==0):
                    #see if you can double push
                    if(rank==1):
                        if(self.grid[8*rank+16+file]==0):
                            moves.append(move.Move(self, p, 8*rank+16+file))
                    if(rank==6):
                        moves.append(move.Move(self, p, 8*rank+8+file, promotion=piece.makepiece(piece.WHITE, piece.QUEEN)))
                        moves.append(move.Move(self, p, 8*rank+8+file, promotion=piece.makepiece(piece.WHITE, piece.ROOK)))
                        moves.append(move.Move(self, p, 8*rank+8+file, promotion=piece.makepiece(piece.WHITE, piece.BISHOP)))
                        moves.append(move.Move(self, p, 8*rank+8+file, promotion=piece.makepiece(piece.WHITE, piece.KNIGHT)))
                    else:
                        moves.append(move.Move(self, p, 8*rank+8+file))
                #capturing
                #not right wall
                if(file != 7):
                    if(self.grid[8*rank+9+file]!=0 and piece.getcolour(self.grid[8*rank+9+file])!=self.turn):
                        if(rank==6):
                            moves.append(move.Move(self, p, 8 * rank + 9 + file, promotion=piece.makepiece(piece.WHITE, piece.QUEEN)))
                            moves.append(move.Move(self, p, 8 * rank + 9 + file, promotion=piece.makepiece(piece.WHITE, piece.ROOK)))
                            moves.append(move.Move(self, p, 8 * rank + 9 + file, promotion=piece.makepiece(piece.WHITE, piece.BISHOP)))
                            moves.append(move.Move(self, p, 8 * rank + 9 + file, promotion=piece.makepiece(piece.WHITE, piece.KNIGHT)))
                        else:
                            moves.append(move.Move(self, p, 8 * rank + 9 + file))
                    #en passant
                    if(self.pawndoublepush == p+1):
                        moves.append(move.Move(self, p, 8*rank+9+file, enpassant=p+1))
                #not left wall
                if(file != 0):
                    if (self.grid[8 * rank + 7 + file] != 0 and piece.getcolour(self.grid[8 * rank + 7 + file]) != self.turn):
                        if (rank == 6):
                            moves.append(move.Move(self, p, 8 * rank + 7 + file, promotion=piece.makepiece(piece.WHITE, piece.QUEEN)))
                            moves.append(move.Move(self, p, 8 * rank + 7 + file, promotion=piece.makepiece(piece.WHITE, piece.ROOK)))
                            moves.append(move.Move(self, p, 8 * rank + 7 + file, promotion=piece.makepiece(piece.WHITE, piece.BISHOP)))
                            moves.append(move.Move(self, p, 8 * rank + 7 + file, promotion=piece.makepiece(piece.WHITE, piece.KNIGHT)))
                        else:
                            moves.append(move.Move(self, p, 8 * rank + 7 + file))
                    # en passant
                    if (self.pawndoublepush == p-1):
                        moves.append(move.Move(self, p, 8 * rank + 7 + file, enpassant=self.pawndoublepush))
        else:
            for p in pawns:
                rank = p//8
                file = p%8
                #pushing forward
                if(self.grid[8*rank-8+file]==0):
                    #see if you can double push
                    if(rank==6):
                        if(self.grid[8*rank-16+file]==0):
                            moves.append(move.Move(self, p, 8*rank-16+file))
                    if(rank==1):
                        moves.append(move.Move(self, p, 8*rank-8+file, promotion=piece.makepiece(piece.BLACK, piece.QUEEN)))
                        moves.append(move.Move(self, p, 8*rank-8+file, promotion=piece.makepiece(piece.BLACK, piece.ROOK)))
                        moves.append(move.Move(self, p, 8*rank-8+file, promotion=piece.makepiece(piece.BLACK, piece.BISHOP)))
                        moves.append(move.Move(self, p, 8*rank-8+file, promotion=piece.makepiece(piece.BLACK, piece.KNIGHT)))
                    else:
                        moves.append(move.Move(self, p, 8*rank-8+file))
                #capturing
                #not right wall
                if(file != 7):
                    if(self.grid[8*rank-7+file]!=0 and piece.getcolour(self.grid[8*rank-7+file])!=self.turn):
                        if(rank==1):
                            moves.append(move.Move(self, p, 8 * rank - 7 + file, promotion=piece.makepiece(piece.BLACK, piece.QUEEN)))
                            moves.append(move.Move(self, p, 8 * rank - 7 + file, promotion=piece.makepiece(piece.BLACK, piece.ROOK)))
                            moves.append(move.Move(self, p, 8 * rank - 7 + file, promotion=piece.makepiece(piece.BLACK, piece.BISHOP)))
                            moves.append(move.Move(self, p, 8 * rank - 7 + file, promotion=piece.makepiece(piece.BLACK, piece.KNIGHT)))
                        else:
                            moves.append(move.Move(self, p, 8 * rank - 7 + file))
                    #en passant
                    if(self.pawndoublepush == p+1):
                        moves.append(move.Move(self, p, 8*rank-7+file, enpassant=p+1))
                #not left wall
                if(file != 0):
                    if (self.grid[8 * rank - 9 + file] != 0 and piece.getcolour(self.grid[8 * rank - 9 + file]) != self.turn):
                        if (rank == 1):
                            moves.append(move.Move(self, p, 8 * rank - 9 + file, promotion=piece.makepiece(piece.BLACK, piece.QUEEN)))
                            moves.append(move.Move(self, p, 8 * rank - 9 + file, promotion=piece.makepiece(piece.BLACK, piece.ROOK)))
                            moves.append(move.Move(self, p, 8 * rank - 9 + file, promotion=piece.makepiece(piece.BLACK, piece.BISHOP)))
                            moves.append(move.Move(self, p, 8 * rank - 9 + file, promotion=piece.makepiece(piece.BLACK, piece.KNIGHT)))
                        else:
                            moves.append(move.Move(self, p, 8 * rank - 9 + file))
                    # en passant
                    if (self.pawndoublepush == p-1):
                        moves.append(move.Move(self, p, 8 * rank - 9 + file, enpassant=p-1))

        #kings
        k = self.pieces[piece.makepiece(self.turn, piece.KING)][0]
        rank = k//8
        file = k%8
        if(self.test(rank-1, file-1)): moves.append(move.Move(self, k, k-9))
        if(self.test(rank-1, file)): moves.append(move.Move(self, k, k-8))
        if(self.test(rank-1, file+1)): moves.append(move.Move(self, k, k-7))
        if(self.test(rank, file-1)): moves.append(move.Move(self, k, k-1))
        if(self.test(rank, file+1)): moves.append(move.Move(self, k, k+1))
        if(self.test(rank+1, file-1)): moves.append(move.Move(self, k, k+7))
        if(self.test(rank+1, file)): moves.append(move.Move(self, k, k+8))
        if(self.test(rank+1, file+1)): moves.append(move.Move(self, k, k+9))

        return moves

    def is_in_check(self):
        k = self.getpieces(piece.makepiece(self.turn, piece.KING))[0]
        self.turn = piece.WHITE if self.turn == piece.BLACK else piece.BLACK
        moves = self.generate_pseudolegal_moves()
        for m in moves:
            if(m.end_square == k):
                self.turn = piece.WHITE if self.turn == piece.BLACK else piece.BLACK
                return True
        self.turn = piece.WHITE if self.turn == piece.BLACK else piece.BLACK
        return False

    def is_in_checkmate(self):
        return self.is_in_check() and len(self.generate_legal_moves())==0

    def filter_for_check(self, moves_):
        not_in_check = []

        # strip moves that put the king in danger away
        for m in moves_:
            legal = True
            colour = self.turn
            self.make_move(m)
            king_pos = self.getpieces(piece.makepiece(colour, piece.KING))[0]
            responses = self.generate_pseudolegal_moves()
            for r in responses:
                if (r.end_square == king_pos):
                    legal = False
            self.unmake_move(m)
            self.turn = colour
            if (legal):
                not_in_check.append(m)

        return not_in_check

    def generate_legal_moves(self):
        moves_ = self.generate_pseudolegal_moves()
        moves = []

        moves.extend(self.filter_for_check(moves_))

        # king side castling
        if (self.turn == piece.WHITE):
            # conditions for castling
            t = self.turn
            if (self.grid[4] == piece.makepiece(piece.WHITE, piece.KING) and self.grid[7] == piece.makepiece(piece.WHITE, piece.ROOK)):
                if (self.timesmoved[4] == 0 and self.timesmoved[7] == 0):
                    if (self.grid[5] == 0 and self.grid[6] == 0):
                        if (not self.is_in_check()):
                            self.grid[5] = self.grid[4]
                            self.grid[4] = 0
                            test = self.is_in_check()
                            self.grid[6] = self.grid[5]
                            self.grid[5] = 0
                            test2 = self.is_in_check()
                            self.grid[4] = self.grid[6]
                            self.grid[6] = 0
                            if ((not test) and (not test2)):
                                # now you can castle
                                moves.append(move.Move(self, 4, 6, castle=True))
                            self.turn = t

        else:
            t = self.turn
            if (self.grid[60] == piece.makepiece(piece.BLACK, piece.KING) and self.grid[63] == piece.makepiece(piece.BLACK, piece.ROOK)):
                if (self.timesmoved[60] == 0 and self.timesmoved[63] == 0):
                    if (self.grid[61] == 0 and self.grid[62] == 0):
                        if (not self.is_in_check()):
                            self.grid[61] = self.grid[60]
                            self.grid[60] = 0
                            test = self.is_in_check()
                            self.grid[62] = self.grid[61]
                            self.grid[61] = 0
                            test2 = self.is_in_check()
                            self.grid[60] = self.grid[62]
                            self.grid[62] = 0
                            if ((not test) and (not test2)):
                                # now you can castle
                                moves.append(move.Move(self, 60, 62, castle=True))
                            self.turn = t

        #queen side castling
        if (self.turn == piece.WHITE):
            # conditions for castling
            t = self.turn
            if (self.grid[4] == piece.makepiece(piece.WHITE, piece.KING) and self.grid[0] == piece.makepiece(piece.WHITE, piece.ROOK)):
                if (self.timesmoved[4] == 0 and self.timesmoved[0] == 0):
                    if (self.grid[3] == 0 and self.grid[2] == 0 and self.grid[1] == 0):
                        if (not self.is_in_check()):
                            self.grid[3] = self.grid[4]
                            self.grid[4] = 0
                            test = self.is_in_check()
                            self.grid[2] = self.grid[3]
                            self.grid[3] = 0
                            test2 = self.is_in_check()
                            self.grid[4] = self.grid[2]
                            self.grid[2] = 0
                            if ((not test) and (not test2)):
                                # now you can castle
                                moves.append(move.Move(self, 4, 2, castle=True))
                            self.turn = t

        else:
            t = self.turn
            if (self.grid[60] == piece.makepiece(piece.BLACK, piece.KING) and self.grid[56] == piece.makepiece(piece.BLACK, piece.ROOK)):
                if (self.timesmoved[60] == 0 and self.timesmoved[56] == 0):
                    if (self.grid[59] == 0 and self.grid[58] == 0 and self.grid[57] == 0):
                        if (not self.is_in_check()):
                            self.grid[59] = self.grid[60]
                            self.grid[60] = 0
                            test = self.is_in_check()
                            self.grid[58] = self.grid[59]
                            self.grid[59] = 0
                            test2 = self.is_in_check()
                            self.grid[60] = self.grid[58]
                            self.grid[58] = 0
                            if ((not test) and (not test2)):
                                # now you can castle
                                moves.append(move.Move(self, 60, 58, castle=True))
                            self.turn = t

        #erase duplicates
        new_moves = []
        for m in moves:
            if(not (m in new_moves)):
                new_moves.append(m)

        return new_moves

    def get_value(self, piecetype):
        d = {
            1: 100,
            2: 500,
            3: 300,
            4: 300,
            5: 900,
            6: 0
        }

        return d[piecetype]

    def generate_captures(self):
        moves = self.generate_legal_moves()
        captures = []

        for m in moves:
            if m.end_piece != 0:
                captures.append(m)

        return captures

    def forcekingtocorner(self, friendlyking, enemyking, endgameweight):
        evaluation = 0

        ekrank = enemyking//8
        ekfile = enemyking%8

        #distance from centre
        evaluation += max(3-ekrank, ekrank-4) + max(3-ekfile, ekfile-4) * 4.7

        fkrank = friendlyking//8
        fkfile = friendlyking%8

        #close kings
        evaluation += (14 - (abs(fkfile-ekfile) + abs(fkrank-ekrank))) * 1.6

        return evaluation * endgameweight

    def count_pieces(self, side):
        c = 0
        for i in self.grid:
            if i != 0 and piece.getcolour(i) == side:
                c += 1

        return c

    def evaluate(self):
        evaluation = 0
        not_turn = piece.WHITE if self.turn == piece.BLACK else piece.BLACK

        friendlyking = self.pieces[piece.makepiece(self.turn, piece.KING)][0]
        enemyking = self.pieces[piece.makepiece(not_turn, piece.KING)][0]
        endgameweight = 20 - self.count_pieces(not_turn)

        #endgame stuff
        evaluation += self.forcekingtocorner(friendlyking, enemyking, endgameweight)

        #who has more pieces
        for p in self.getpieces(piece.makepiece(self.turn, piece.PAWN)):
            evaluation += self.get_value(piece.PAWN)
            if(self.turn == piece.WHITE):
                evaluation += PAWNTABLEWHITE[p]
            else:
                evaluation += PAWNTABLEBLACK[p]
        for r in self.getpieces(piece.makepiece(self.turn, piece.ROOK)):
            evaluation += self.get_value(piece.ROOK)
        for k in self.getpieces(piece.makepiece(self.turn, piece.KNIGHT)):
            evaluation += self.get_value(piece.KNIGHT) + KNIGHTTABLE[k]
        for b in self.getpieces(piece.makepiece(self.turn, piece.BISHOP)):
            evaluation += self.get_value(piece.BISHOP) + BISHOPTABLE[b]
        for q in self.getpieces(piece.makepiece(self.turn, piece.QUEEN)):
            evaluation += self.get_value(piece.QUEEN) + QUEENTABLE[q]

        for p in self.getpieces(piece.makepiece(not_turn, piece.PAWN)):
            evaluation -= self.get_value(piece.PAWN)
            if(not_turn == piece.WHITE):
                evaluation -= PAWNTABLEWHITE[p]
            else:
                evaluation -= PAWNTABLEBLACK[p]
        for r in self.getpieces(piece.makepiece(not_turn, piece.ROOK)):
            evaluation -= self.get_value(piece.ROOK)
        for k in self.getpieces(piece.makepiece(not_turn, piece.KNIGHT)):
            evaluation -= self.get_value(piece.KNIGHT) + KNIGHTTABLE[k]
        for b in self.getpieces(piece.makepiece(not_turn, piece.BISHOP)):
            evaluation -= self.get_value(piece.BISHOP) + BISHOPTABLE[b]
        for q in self.getpieces(piece.makepiece(not_turn, piece.QUEEN)):
            evaluation -= self.get_value(piece.QUEEN) + QUEENTABLE[q]

        return evaluation

    def search_captures(self, alpha, beta):
        evaluation = self.evaluate()
        if(evaluation >= beta):
            return beta
        alpha = max(alpha, evaluation)

        moves = self.order_moves(self.generate_captures())

        for m in moves:
            self.make_move(m)
            evaluation = -self.search_captures(-beta, -alpha)
            self.unmake_move(m)

            if(evaluation >= beta):
                return beta
            alpha = max(alpha, evaluation)

        return alpha

    def search(self, depth, alpha, beta, move=None):
        if(depth==0):
            return self.search_captures(alpha, beta), move, 1

        moves = self.generate_legal_moves()

        if(len(moves) == 0):
            if(self.is_in_check()):
                return -float("inf"), move, 1
            return 0, move, 1

        moves = self.order_moves(moves)

        bestmove = None
        searches = 0

        for m in moves:
            self.make_move(m)
            e, _, s = self.search(depth-1, -beta, -alpha, move=m)
            searches += s
            self.unmake_move(m)
            e = -e
            if(e >= beta):
                return beta, m, searches

            if(e > alpha):
                alpha = e
                bestmove = m

        return alpha, bestmove, searches

    def order_moves(self, moves):
        new_moves = []

        for m in moves:
            #value_guess is going to decrease so the best moves are first
            value_guess = 0
            start_type = piece.gettype(m.start_piece)
            end_type = piece.gettype(m.end_piece)

            #if it's a capture
            if(m.end_piece != 0 and end_type != piece.KING):
                value_guess -= 10 * self.get_value(end_type) - self.get_value(start_type)

            #promotions are probably good
            if(m.promotion != m.start_piece):
                value_guess -= self.get_value(piece.gettype(m.promotion))

            new_moves.append([m, value_guess])

        #sort the moves
        new_moves.sort(key=lambda l: l[1])
        new_moves = list(map(lambda l: l[0], new_moves))

        return new_moves


    def ai(self):
        test1, m, _ = self.search(2, -float("inf"), float("inf"))
        if(test1 == float("inf")):
            print(_)
            return m
        _, m, s = self.search(4, -float("inf"), float("inf"))
        print(s)
        if(m is None):
            if(len(self.generate_legal_moves()) != 0):
                return self.generate_legal_moves()[0]
        return m