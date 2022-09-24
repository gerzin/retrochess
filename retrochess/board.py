from enum import Enum
from typing import List, Tuple, Union

class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"

class PieceType(str, Enum):
    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"

    def __str__(self) -> str:
        return f"{self.value}"


class Piece():
    def __init__(self, ptype, pcolor):
        self.type_: PieceType = ptype
        self.color_: PieceColor = pcolor
    
    @property
    def color(self):
        return self.color_
    
    @property
    def type(self):
        return self.type_

    def __str__(self):
        return str(self.type_).capitalize() if self.color_ == PieceColor.BLACK else str(self.type_)



def is_in(p0, p1):
    return (0<= p0<8) and (0 <= p1 < 8)

class GameState():
    def __init__(self):
        self.white_can_castle_short = True
        self.black_can_castle_short = True
        self.white_can_castle_long = True
        self.black_can_castle_long = True
        self.white_in_check = False
        self.black_in_check = False
        self.white_turn = True
        self.fisher_random    = False
        self.__selected_piece = None
        self.__selected_piece_possible_moves = None
        self.__moves = []
        self.last_move = None
    
    @property
    def selected_piece(self):
        return self.__selected_piece
    
    @property
    def possible_moves(self):
        return self.__selected_piece_possible_moves
    
    @possible_moves.setter
    def possible_moves(self, moves_list: Union[List[Tuple[int, int]], None]):
        self.__selected_piece_possible_moves = moves_list
    
    @selected_piece.setter
    def selected_piece(self, coord: Union[Tuple[int, int] , None]):
        self.__selected_piece = coord
        if coord is None:
            self.possible_moves = None
    
    @property
    def moves(self):
        return self.__moves
    
    
    def add_move(self, move):
        if self.white_turn:
            self.moves.append((move, None))
        else:
            self.moves[-1] = (self.moves[-1][0], move)

class Board():
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.__state = GameState()
        self.__board = self._init_board()
    
    @property
    def board(self) -> List[Piece | None]:
        return self.__board
    
    @property
    def state(self) -> GameState:
        return self.__state

    def _init_board(self):
        board = []
        create_pawns = lambda color: [Piece(PieceType.PAWN, color)] * 8
        create_pieces = lambda color: [Piece(t, color) for t in [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN, PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]]
        
        white_pawns = create_pawns(PieceColor.WHITE)
        black_pawns = create_pawns(PieceColor.BLACK)
        white_pieces = create_pieces(PieceColor.WHITE)
        black_pieces = create_pieces(PieceColor.BLACK)

        
        board.append(black_pieces)
        board.append(black_pawns)
        for _ in range(4):
            board.append([None]*8)
        board.append(white_pawns)
        board.append(white_pieces)

        return board
    
    def select(self, row:int, col:int):
        piece = self.at(row, col)
        turn = PieceColor.WHITE if self.state.white_turn else PieceColor.BLACK
        # the cell is not empty
        if piece:
            # if that cell was not already selected and the piece is of the right color
            if (row, col) != self.state.selected_piece and piece.color == turn:
                self.state.selected_piece = (row, col)
                self.state.possible_moves = self.generate_possible_moves((row,col))
            else:
                self.state.selected_piece = None
                self.state.possible_moves = None
        else:
            self.state.selected_piece = None
            self.state.possible_moves = None

    def can_move(self, src_pos, dest_pos) -> bool:
        sx, sy = src_pos
        src_piece = self.board[sx][sy]
        
        if src_piece:
            if dest_pos in self.state.possible_moves:
                return True
        else:
            return False
    
    def generate_possible_moves(self, src_pos):
        sx, sy = src_pos
        src_piece: Piece = self.board[sx][sy]
        moves = []

        if (src_piece.color == PieceColor.WHITE and not self.state.white_turn) or (src_piece.color == PieceColor.BLACK and self.state.white_turn):
            return moves
        

        def diagonal_moves(max_range=8):
            # look on the four diagonals
            for i in range(1,max_range):
                point = (sx-i, sy-i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break

            for i in range(1,max_range):
                point = (sx-i, sy+i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
            for i in range(1,max_range):
                point = (sx+i, sy-i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
            for i in range(1,max_range):
                point = (sx+i, sy+i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
        
        def horizontal_moves(max_range=8):
            for i in range(1, max_range):
                point = (sx, sy-i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
            for i in range(1, max_range):
                point = (sx, sy+i)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
            
            for i in range(1, max_range):
                point = (sx-i, sy)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
            
            for i in range(1, max_range):
                point = (sx+i, sy)
                if is_in(*point):
                    p = self.at(*point)
                    if p is None:
                        moves.append(point)
                    else:
                        if p.color != src_piece.color:
                            moves.append(point)
                        break
                
        # PAWN MOVES
        if src_piece.type == PieceType.PAWN:
            if src_piece.color == PieceColor.WHITE:
                # advance
                if is_in(sx-1, sy) and self.at(sx-1, sy) is None:
                    moves.append((sx-1, sy))
                    if sx == 6 and self.at(sx-2, sy) is None:
                        moves.append((sx-2, sy))
                # take enemy piece
                for y in (sy-1, sy+1):
                    if is_in(sx-1, y):
                        p = self.at(sx-1,y)
                        if p is not None and p.color != src_piece.color:
                            moves.append((sx-1, y)) 
                
            else:
                # advance
                if is_in(sx+1, sy) and self.at(sx+1, sy) is None:
                    moves.append((sx+1, sy))
                    if sx == 1 and self.at(sx+2, sy) is None:    
                        moves.append((sx+2, sy))
               # take enemy piece
                for y in (sy-1, sy+1):
                    if is_in(sx+1, y):
                        p = self.at(sx+1,y)
                        if p is not None and p.color != src_piece.color:
                            moves.append((sx+1, y))
        # KNIGHT MOVES
        elif src_piece.type == PieceType.KNIGHT:    
            for candidate_move in [(sx+2, sy-1), (sx+2, sy+1), (sx-2, sy-1), (sx-2, sy+1), (sx-1, sy-2), (sx-1, sy+2), (sx+1, sy-2), (sx+1, sy+2)]:
                if is_in(*candidate_move):
                    p = self.at(*candidate_move)
                    if p and p.color == src_piece.color:
                        pass
                    else:
                        moves.append(candidate_move)
        # BISHOP MOVES
        elif src_piece.type is PieceType.BISHOP:
            diagonal_moves()
        # ROOK MOVE
        elif src_piece.type is PieceType.ROOK:
            horizontal_moves()
        # QUEEN MOVES
        elif src_piece.type is PieceType.QUEEN:
            diagonal_moves()
            horizontal_moves()
        # KING MOVES
        elif src_piece.type is PieceType.KING:
            diagonal_moves(max_range=2)
            horizontal_moves(max_range=2)
            # cannot move in position under checks

            # add castling
        
        
        return moves
    
    def move(self, src, dest):
        sx, sy = src
        dx, dy = dest
        self.state.add_move(self.__generate_move_name(src, dest))
        self.board[sx][sy], self.board[dx][dy] = None, self.board[sx][sy]
        self.state.selected_piece = None
        self.state.possible_moves = None
        
        self.state.white_turn = not self.state.white_turn
        self.state.last_move = (src, dest)
    
    def __generate_move_name(self, src, dest, castle=None):

        if castle:
            if castle == 's':
                return "O-O"
            else:
                return "O-O-O"

        def coord_to_cell_name(x,y):  
            return f"{'abcdefgh'[y]}{8-x}"

        src_piece = self.at(*src)
        dest_piece = self.at(*dest)

        move = "{piece}{src_square}{takes}{dest}{promotion}{check}{checkmate}"

        piece = src_piece.type.value.capitalize() if src_piece.type.value != PieceType.PAWN else coord_to_cell_name(*src)[0]
        src_square   = ""
        takes = "x" if dest_piece else ""
        dest = coord_to_cell_name(*dest)
        promotion = ""
        check = ""
        checkmate = ""
        move_string = move.format(piece=piece, src_square=src_square, takes=takes, dest=dest, promotion=promotion, check=check, checkmate=checkmate)
        return move_string if move_string[0] != move_string[1] else move_string[1:]


    def at(self, p0, p1):
        return self.board[p0][p1]
                
    



