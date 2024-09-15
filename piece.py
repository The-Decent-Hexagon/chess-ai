import pygame as pg

WHITE = 0
BLACK = 1
PAWN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6

def makepiece(colour, type):
    return type + colour * 7

def gettype(piece):
    return piece%7

def getcolour(piece):
    return piece//7

def getimage(piece):
    image_link = "image_"
    if(getcolour(piece) == WHITE):
        image_link += "0-"
    else:
        image_link += "1-"

    t = gettype(piece)
    if(t == KING): image_link += "0.png"
    if(t == QUEEN): image_link += "1.png"
    if(t == BISHOP): image_link += "2.png"
    if(t == KNIGHT): image_link += "3.png"
    if(t == ROOK): image_link += "4.png"
    if(t == PAWN): image_link += "5.png"

    return pg.image.load(image_link).convert_alpha()