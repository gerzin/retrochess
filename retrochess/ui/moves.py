from typing import List
from pygame.surface import Surface
import pygame

from ui.config import Config

class MovesViewer():
    def __init__(self, moves_list: List, surface:Surface) -> None:
        self.__surface = surface
        self.__moves = moves_list
        self.font = pygame.font.Font(Config.assets.FONTS / "font0.ttf", 14)
    
    @property
    def surface(self):
        return self.__surface
    
    def update(self):
        self.surface.fill(Config.color.LIGHT)

        if self.__moves:
            render_move = lambda i, x : self.font.render(f"{i}. {x}", True, Config.color.TEXT_COLOR, Config.color.DARK)
            moves = [self.__moves_to_text(m) for m in self.__moves]
            moves_txt = [render_move(i, x) for i,x in enumerate(moves, start=1)]
            self.surface.blit(moves_txt[-1], (10,10))
        else:
            text = self.font.render("Make a move to start the game", True, Config.color.TEXT_COLOR)
            self.surface.blit(text, (10,10))
        
        
        
    
    def __moves_to_text(self, move):
        if move[1]:
            return f"{move[0]} {move[1]}"
        else:
            return f"{move[0]} ---"