import itertools

class InvalidFexException(Exception):
    pass

from ctypes import Union
from curses.ascii import isupper
from typing import List
from board import Board, Piece, PieceColor, PieceType

letter_to_type = {
    'p' : PieceType.PAWN,
    'n' : PieceType.KNIGHT,
    'b' : PieceType.BISHOP,
    'r' : PieceType.ROOK,
    'q' : PieceType.QUEEN,
    'k' : PieceType.KING
}

def char_to_piece_list(c: str) -> List[Piece]:
    if c.isdigit():
        return [None]*int(c)
    else:
        if c.isupper():
            color = PieceColor.WHITE
        else:
            color = PieceColor.BLACK
        
        pt = letter_to_type[c.lower()]
        return[Piece(pt, color)]
        

def fen_to_board(fen_str: str):
    rows, rest = fen_str.split(" ")
    rows = rows.split("/")
    board_list = [list(itertools.chain(*[char_to_piece_list(c) for c in r])) for r in rows]
    return board_list


def board_to_fen(board) -> str:
    pass
