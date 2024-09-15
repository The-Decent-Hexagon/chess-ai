import time

import pygame as pg
import pygame.key

import board
import piece
import move
b = board.Board()

AIPLAYS = piece.BLACK

b.startingposition()

"""b.grid[20] = piece.makepiece(piece.WHITE, piece.KING)
b.grid[44] = piece.makepiece(piece.BLACK, piece.KING)
b.grid[52] = piece.makepiece(piece.BLACK, piece.ROOK)
b.grid[60] = piece.makepiece(piece.BLACK, piece.ROOK)"""

"""b.grid[5] = 0
b.grid[6] = 0
b.grid[11] = 0
b.grid[12] = piece.makepiece(piece.WHITE, piece.KNIGHT)
b.grid[13] = piece.makepiece(piece.BLACK, piece.KNIGHT)
b.grid[26] = piece.makepiece(piece.WHITE, piece.BISHOP)
b.grid[42] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[50] = 0
b.grid[51] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[52] = piece.makepiece(piece.BLACK, piece.BISHOP)
b.grid[60] = 0
b.grid[61] = piece.makepiece(piece.BLACK, piece.KING)
b.grid[62] = 0

b.update_lists()

def count(depth):
    if depth == 0:
        return 1

    c = 0
    for m in b.generate_legal_moves():
        t = b.turn
        b.make_move(m)
        ct = count(depth-1)
        c += ct
        b.unmake_move(m)
        b.turn = t

    return c

print(count(4))"""

"""b.grid[5*8+5]=piece.makepiece(piece.WHITE, piece.QUEEN)
b.grid[6*8+6]=piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[7*8+3]=piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[1*8+1]=piece.makepiece(piece.BLACK, piece.PAWN)"""

"""b.grid[1] = piece.makepiece(piece.WHITE, piece.QUEEN)
b.grid[3] = piece.makepiece(piece.WHITE, piece.ROOK)
b.grid[4] = piece.makepiece(piece.BLACK, piece.ROOK)
b.grid[13] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[14] = piece.makepiece(piece.WHITE, piece.KING)
b.grid[17] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[21] = piece.makepiece(piece.WHITE, piece.KNIGHT)
b.grid[23] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[26] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[30] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[31] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[32] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[35] = piece.makepiece(piece.WHITE, piece.PAWN)
b.grid[36] = piece.makepiece(piece.BLACK, piece.QUEEN)
b.grid[41] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[46] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[53] = piece.makepiece(piece.BLACK, piece.PAWN)
b.grid[60] = piece.makepiece(piece.BLACK, piece.ROOK)
b.grid[62] = piece.makepiece(piece.BLACK, piece.KING)"""


b.update_lists()

#boring pygame initialisation stuff
pg.init()
WINSIZE = 1250
WHITE = (200, 200, 200)
BLACK = (100, 100, 100)
window = pg.display.set_mode((WINSIZE, WINSIZE))
clock = pg.time.Clock()
running = True
mousepressed = False
squareclicked = None
squareunclicked = None
mostrecentmove = None
promotionpiece = None
while running:
    if (b.is_in_checkmate()):
        print(f"{'white' if b.turn == piece.BLACK else 'black'} wins!")
        while True:
            pass
    if(b.turn == AIPLAYS):
        m = b.ai()
        mostrecentmove = m
        if(mostrecentmove is None):
            print("stalemate")
            while True:
                pass
        b.make_move(m)
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            running = False
            pg.quit()
        elif(event.type == pg.KEYDOWN):
            if(event.key == pg.K_q):
                promotionpiece = piece.QUEEN
            elif(event.key == pg.K_r):
                promotionpiece = piece.ROOK
            elif(event.key == pg.K_b):
                promotionpiece = piece.BISHOP
            elif(event.key == pg.K_k):
                promotionpiece = piece.KNIGHT
            elif(event.key == pg.K_c):
                print(b.is_in_check())

        elif(event.type == pg.KEYUP):
            promotionpiece = None

    #time to deal with mouse
    if(pg.mouse.get_pressed(3)[0] == True):
        if(mousepressed == False):
            #just clicked
            mousepressed = True
            x, y = pg.mouse.get_pos()
            i, j = x//(WINSIZE/8), y//(WINSIZE/8)
            if(b.grid[int((7-j)*8+i)] != 0):
                #clicked piece, important
                squareclicked = int((7-j)*8+i)
                #print(chr(97+squareclicked%8+1) + str(squareclicked//8))
    else:
        if(mousepressed == True):
            #just unclicked
            mousepressed = False
            if(squareclicked != None):
                x, y = pg.mouse.get_pos()
                i, j = x // (WINSIZE / 8), y // (WINSIZE / 8)
                squareunclicked = int((7-j)*8+i)
                tempmrm = mostrecentmove
                mostrecentmove = move.Move(b, squareclicked, squareunclicked, promotion=promotionpiece)
                plm = b.generate_legal_moves()
                if(mostrecentmove in plm):
                    index = plm.index(mostrecentmove)
                    b.make_move(plm[index])
                    mostrecentmove = plm[index]
                    #print(b.turn)
                else:
                    mostrecentmove = tempmrm
                squareclicked = None
                #print(b.generate_pseudolegal_moves())
                #print(len(b.generate_legal_moves()))

    #b.make_move(b.ai())

    #render the board you get me
    for i in range(8):
        for j in range(8):
            if(j%2==i%2):
                colour = WHITE #it might be white
            else:
                colour = BLACK #it might be black
            if(not (mostrecentmove is None)):
                if(mostrecentmove.start_square == (7-i)*8+j):
                    colour = (0,255,0)
                elif(mostrecentmove.end_square == (7-i)*8+j):
                    colour = (255,0,0)
            x = j*WINSIZE/8
            y = i*WINSIZE/8
            pg.draw.rect(window, colour, pg.Rect(x, y, WINSIZE/8, WINSIZE/8))
            square = (7-i)*8+j
    #draw the pieces you get me
    for i in range(8):
        for j in range(8):
            x = j*WINSIZE/8
            y = i*WINSIZE/8
            square = (7-i)*8+j
            # draw the piece
            if (b.grid[square] != 0):
                if (square == squareclicked):
                    x, y = pg.mouse.get_pos()
                    x -= WINSIZE / 16
                    y -= WINSIZE / 16
                window.blit(piece.getimage(b.grid[square]), (x, y))

    pg.display.flip()
    clock.tick(144)