from typing import List
from pygame.surface import Surface
import pygame
from board import Board

from ui.config import Config


class MovesViewer():
    def __init__(self, board: Board, surface:Surface) -> None:
        self.board = board
        self.__surface = surface
        self.font = pygame.font.Font(Config.assets.FONTS / "font0.ttf", 14)
        self.moves_subs = Surface.subsurface(self.surface, (1, 1, self.surface.get_width() - 1, self.surface.get_height() - 1))
        self.max_fitting_moves = self.moves_subs.get_height() // self.font.get_height()
        self.init_banner()
    
    def init_banner(self):
        self.banner_infos = []
        text_0 = self.font.render("Make a move to", True, Config.color.TEXT_COLOR)
        text_1 = self.font.render("start a new game", True, Config.color.TEXT_COLOR)
        text_press = self.font.render("press:", True, Config.color.TEXT_COLOR)
        commands = [self.font.render(x, True, Config.color.TEXT_COLOR) for x in "* r - reset,* f - flip".split(",")]
        
        for x in (text_0, text_1, text_press, *commands):
            self.banner_infos.append(x)
    
    @property
    def surface(self):
        return self.__surface
    
    def update(self):
        self.surface.fill(Config.color.LIGHT)

        if self.board.state.moves:
            self.__render_moves(self.moves_subs)
        else:
            self.__show_banner()
    
    def __render_moves(self, subsurface):
        
        __moves = self.board.state.moves

        render_move = lambda i, x : self.font.render(f"{str(i)+'.':>3} {x:<}", True, Config.color.TEXT_COLOR)
        render_move_highlight = lambda i, x : self.font.render(f"{str(i)+'.':<3} {x:<}", True, Config.color.TEXT_COLOR, Config.color.DARK)
        moves = [self.__moves_to_text(m) for m in __moves[-self.max_fitting_moves:]]
        
        start_index = max(1, len(__moves) - self.max_fitting_moves+1)

        moves_txt = [render_move(i, x) for i,x in enumerate(moves[:-1], start=start_index)] + [render_move_highlight(len(__moves), moves[-1])]
        fh = self.font.get_height()
        for i, move_txt in enumerate(moves_txt):
            subsurface.blit(move_txt, (10, i * fh))
        
    def __show_banner(self):
        
        for i, text in enumerate(self.banner_infos[:2]):
            self.surface.blit(text, (10,10+i*self.font.get_height()))
        
        for i, text in enumerate(self.banner_infos[2:], start=3):
            self.surface.blit(text, (10,12+i*self.font.get_height()))
        

        
    
    
    def __moves_to_text(self, move):
        if move[1]:
            return f"{move[0]:6} {move[1]:6}"
        else:
            return f"{move[0]:6} {'---':6}"