from typing import Tuple
import pygame
from board import Board, Piece, PieceColor, PieceType
from pygame.surface import Surface
from math import floor
from pathlib import Path
from pygame.transform import flip as Flip

from ui.config import Config


def load_and_scale(path, scale:Tuple = (62, 62)):
    return pygame.transform.scale(pygame.image.load(path), scale)


class PieceViewer:

    def __init__(self, **kwargs):
        scale = kwargs.get("scale", (62, 62))
        self.set_path = Config.assets.PIECES / "pixel"
        self.flipped = kwargs.get("flipped", False)
        self.type_img_white = {
            PieceType.PAWN: load_and_scale(self.set_path / "wP.svg", scale),
            PieceType.KNIGHT.value: load_and_scale(self.set_path / "wN.svg", scale),
            PieceType.BISHOP.value: load_and_scale(self.set_path / "wB.svg", scale),
            PieceType.ROOK.value: load_and_scale(self.set_path / "wR.svg", scale),
            PieceType.QUEEN.value: load_and_scale(self.set_path / "wQ.svg", scale),
            PieceType.KING.value: load_and_scale(self.set_path / "wK.svg", scale)
        }

        self.type_img_black = {
            PieceType.PAWN: load_and_scale(self.set_path / "bP.svg", scale),
            PieceType.KNIGHT.value: load_and_scale(self.set_path / "bN.svg", scale),
            PieceType.BISHOP.value: load_and_scale(self.set_path / "bB.svg", scale),
            PieceType.ROOK.value: load_and_scale(self.set_path / "bR.svg", scale),
            PieceType.QUEEN.value: load_and_scale(self.set_path / "bQ.svg", scale),
            PieceType.KING.value: load_and_scale(self.set_path / "bK.svg", scale)
        }

    
    def draw_piece(self, piece: Piece, srf: Surface):
        pt = piece.type_
        
        if piece.color == PieceColor.BLACK:
            srf.blit(Flip(self.type_img_black[pt], self.flipped, self.flipped), (0,0))
        else:
            srf.blit(Flip(self.type_img_white[pt], self.flipped, self.flipped), (0,0))
        
        

def alternate_colors(*args):
    a = [*args]
    while True:
        for ar in a:
            yield a
    

class BoardViewer():
    
    def __init__(self, board: Board, surface: Surface) -> None:
        self.__board: Board = board
        self.__surface = surface
        self.__flipped = False

        self.square_size = surface.get_width() / 8

        self.light_color = Config.color.LIGHT
        self.dark_color = Config.color.DARK

        self.piece_viewer = PieceViewer(scale=(surface.get_width() / 8, surface.get_height() / 8))
        # font for drawing the letters
        self.font = pygame.font.Font(Config.assets.FONTS / "font0.ttf", int(self.square_size / 6))
        colors = [Config.color.LIGHT, Config.color.DARK]
        self.square_letters = [self.font.render(x, True, colors[i%2]) for i,x in enumerate("abcdefgh")]
        self.square_letters_flipped = [Flip(self.font.render(x, True, colors[(i+1)%2]), True, True) for i,x in enumerate("abcdefgh")]
        self.square_numbers = [self.font.render(x, True, colors[i%2]) for i,x in enumerate("87654321")]
        self.square_numbers_flipped = [Flip(self.font.render(x, True, colors[i%2]), True, True) for i,x in enumerate("12345678")]

        # mouse related variables
        self.track_mouse = True # if True highlight the cell under the mouse
        self.mouse_pos = None
        self.show_selected_cell = True
    
    @property
    def surface(self):
        return self.__surface
    
    @surface.setter
    def surface(self, new_srf):
        self.__surface = new_srf
    
    @property
    def flipped(self):
        return self.__flipped
    
    def flip(self):
        self.__flipped = not self.__flipped
        self.piece_viewer.flipped = self.__flipped
    
    @property
    def board(self) -> Board:
        return self.__board
    
    def __draw_grid(self):
        srf = self.surface
        srf.fill(self.dark_color)
        
        def draw_light_squares(srf, ss):
            for col in range(8):
                if col % 2 :
                    for row in (1,3,5,7):
                        pygame.draw.rect(srf, self.light_color, (row*ss, col*ss ,ss, ss))
                else:
                    for row in range(4):
                        pygame.draw.rect(srf, self.light_color, (row*2*ss, col*ss ,ss, ss))
        
        
        
        draw_light_squares(srf, self.square_size)

    def __draw_pieces(self):
        board = self.board.board
        for i in range(8):
            for j in range(8):
                if p:= board[i][j]:
                    subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(i,j))
                    self.piece_viewer.draw_piece(p, subs)


    def __draw_highlited_cell(self):
        if self.mouse_pos and self.track_mouse:
            i,j = self.mouse_coords_to_board_cell(self.mouse_pos)
            subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(j,i))
            subs.fill(Config.color.HIGHLIGHT)
    
    def __draw_selected_cell(self):
        if self.show_selected_cell:
            if sc:= self.__board.state.selected_piece:
                Surface.subsurface(self.surface, self.__coords_to_square_rect(sc[0], sc[1])).fill(Config.color.SELECTION)
    
    def __draw_possible_moves(self):
        if self.board.state.possible_moves:
            for p in self.board.state.possible_moves:
                subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(*p))
                subs.fill(Config.color.SELECTION)
    
    def __draw_last_move(self):
        lm = self.board.state.last_move
        if lm:
            Surface.subsurface(self.surface, self.__coords_to_square_rect(*lm[0])).fill(Config.color.LAST_MOVE)
            Surface.subsurface(self.surface, self.__coords_to_square_rect(*lm[1])).fill(Config.color.LAST_MOVE)
    
    def __draw_coordinates(self):
        

        
        
        if self.flipped:
            letter_pos_x = self.square_size - self.square_letters_flipped[0].get_width() - 2
            letter_pos_y = 2
            number_pos_y = self.square_size-self.font.get_height() - 2
            
            for i in range(8):
                letter = self.square_letters_flipped[i]
                number = self.square_numbers_flipped[7-i]
                subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(0,i))
                subs.blit(letter,(letter_pos_x, letter_pos_y))
                
                subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(i,0))
                subs.blit(number,(2, number_pos_y))

        else:
            letter_pos_y = self.square_size - self.font.get_height() - 2
            number_pos_x = self.square_size - self.square_letters[0].get_width() - 2
            for i in range(8):
                letter = self.square_letters[i]
                number = self.square_numbers[i]
                subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(7,i))
                subs.blit(letter ,(2, letter_pos_y))
                subs = Surface.subsurface(self.surface, self.__coords_to_square_rect(i,7))
                subs.blit(number,(number_pos_x, 2))
                

    
    def __coords_to_square_rect(self, i:int,j:int) -> pygame.Rect:
        """Given col,row coordinates, return the corresponding square on the chessboard

        Args:
            i (int): Column index
            j (int): Row index
        Returns:
            pygame.Rect: _description_
        """
        return pygame.Rect(j*self.square_size, i*self.square_size, self.square_size, self.square_size)
    
    def on_mouse_on(self, mouse_pos):
        self.mouse_pos = mouse_pos

    def on_mouse_off(self, mouse_pos):
        self.mouse_pos = None
          

    def update(self):
        self.__draw_grid()
        self.__draw_highlited_cell()
        self.__draw_selected_cell()
        self.__draw_last_move()
        self.__draw_possible_moves()
        self.__draw_coordinates()
        self.__draw_pieces()

        if self.flipped:
            self.surface = Flip(self.surface, True, True)
    

    def mouse_coords_to_board_cell(self, mouse_coords) -> Tuple[int, int]:
        """Transform mouse coordinates to cell's indices

        Args:
            mouse_coords (Tuple[int, int]): mouse coordinates

        Returns:
            Tuple[int, int]: col and row
        """
        x, y = mouse_coords
        x //= self.square_size
        y //= self.square_size
        x = int(x)
        y = int(y)
        return (7-x, 7-y) if self.flipped else (x,y)