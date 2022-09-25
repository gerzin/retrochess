from pygame.surface import Surface
import pygame
from board import Board
from ui.config import Config

class TimerViewer():
    def __init__(self, board: Board, surface:Surface) -> None:
        self.__surface = surface
        self.board = board
        # mouse related variables
        self.mouse_pos = None
        self.font = pygame.font.Font(Config.assets.FONTS / "font0.ttf", int(self.__surface.get_height() / 4))
    
    @property
    def surface(self):
        return self.__surface
    
    def update(self):
        if self.mouse_pos:
            self.surface.fill(Config.color.DARK)
        else:
            self.surface.fill(Config.color.LIGHT)
    
    def on_mouse_on(self, mouse_pos):
        self.mouse_pos = mouse_pos

    def on_mouse_off(self, mouse_pos):
        self.mouse_pos = None