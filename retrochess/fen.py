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

type_to_letter = {v: k for k, v in letter_to_type.items()}

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

def piece_to_char(p: Piece):
    if p.color == PieceColor.BLACK:
        return type_to_letter[p.type]
    else:
        return type_to_letter[p.type].upper()

def fen_to_board(fen_str: str):
    rows, rest = fen_str.split(" ")
    rows = rows.split("/")
    board_list = [list(itertools.chain(*[char_to_piece_list(c) for c in r])) for r in rows]
    return board_list


def board_to_fen(board) -> str:
    fen_str = ""
    rows = []
    for row in board.board:
        row_fen = ""
        counter = 0
        for piece in row:
            if piece:
                fen_str += piece_to_char(piece)
                if counter:
                    row_fen += str(counter)
                    counter = 0
            else:
                counter += 1
        if counter:
            row_fen += str(counter)
        rows.append(row_fen)
    return "/".join(rows)
        

