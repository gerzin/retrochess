import pygame
from pygame.surface import Surface
from board import Board
from fen import board_to_fen
from ui.config import Config

class FenViewer:
    def __init__(self, board: Board, surface: Surface) -> None:
        self.__surface = surface
        self.board = board
        self.font = pygame.font.Font(Config.assets.FONTS / "font0.ttf", int(self.__surface.get_height() - 4))
        self.fen_string = f"FEN: {board_to_fen(self.board)}"
        self.last_move_len = None
    
    @property
    def surface(self):
        return self.__surface

    def update(self):
        self.surface.fill(Config.color.LIGHT)
        # compute the new fen only on board changes
        if self.board.state.moves[-1:] != self.last_move_len:
            self.last_move_len = self.board.state.moves[-1:]
            self.fen_string = f"FEN: {board_to_fen(self.board)}"
        self.surface.blit(self.font.render(self.fen_string, True, (0,0,0)), (0,0))