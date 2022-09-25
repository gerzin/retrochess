#!/usr/bin/env python3
import pygame
import atexit
from board import Board
from ui.moves import MovesViewer
from ui.timer import TimerViewer
from ui.board import BoardViewer
from ui.config import Config
from pygame.color import Color

BOARD_SIZE = 520
assert BOARD_SIZE % 8 == 0

BOARD_OFFSET = (2*Config.SPACING, 2*Config.SPACING)
TIMER_OFFSET = (4*Config.SPACING + BOARD_SIZE, 2*Config.SPACING)
MOVES_OFFSET = (TIMER_OFFSET[0], TIMER_OFFSET[1] + BOARD_SIZE / 4 + 20)

def mouse_to_surface(mouse_pos, surface_offset):
    return (mouse_pos[0]-surface_offset[0], mouse_pos[1]-surface_offset[1])



def main():
    pygame.init()
    atexit.register(pygame.quit)

    screen = pygame.display.set_mode((850, 560))
    pygame.display.set_caption('RetroChess')

    # board creation
    board_size = BOARD_SIZE
    board_surface = pygame.Surface((board_size, board_size))
    board = Board()
    board_viewer = BoardViewer(board, board_surface)

    # timer creation
    timer_surface_w = (board_size) / 2
    timer_surface_h = (board_size) / 4
    timer_surface = pygame.Surface((timer_surface_w, timer_surface_h))

    timer_viewer = TimerViewer(timer_surface)

    # moves viewer creation
    moves_viewer_surface_w = timer_surface_w
    moves_viewer_surface_h = 560 - 60 - timer_surface_h
    moves_viewer_surface = pygame.Surface((moves_viewer_surface_w, moves_viewer_surface_h))
    moves_viewer = MovesViewer(board, moves_viewer_surface)

    running = True
    
    while running:
        event = pygame.event.wait(1000)

        if event.type == pygame.QUIT:
            running = False
            continue

        # dispatch the events
        if event.type == pygame.MOUSEMOTION:
            abs_mouse_pos = pygame.mouse.get_pos()
            # handle board
            mouse_pos = mouse_to_surface(abs_mouse_pos, BOARD_OFFSET)
            if board_surface.get_rect().collidepoint(mouse_pos):
                board_viewer.on_mouse_on(mouse_pos)
            else:
                board_viewer.on_mouse_off(mouse_pos)
            # handle timer

            # handle moves history


        elif event.type == pygame.MOUSEBUTTONUP:
            pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            abs_mouse_pos = pygame.mouse.get_pos()
            # handle board
            mouse_pos = mouse_to_surface(abs_mouse_pos, BOARD_OFFSET)
            # right click unselect things
            if event.button == pygame.BUTTON_RIGHT:
                board.state.selected_piece = None

            elif board_surface.get_rect().collidepoint(mouse_pos):
                (y,x) = board_viewer.mouse_coords_to_board_cell(mouse_pos)
                if board.state.selected_piece != None:
                    if board.can_move(board.state.selected_piece, (x,y)): # check if that's a move
                        board.move(board.state.selected_piece, (x,y))
                    else:
                        board.select(x, y)
                else:
                    board.select(x, y)
            else:
                board.state.selected_piece = None
        
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_r:
                    board.reset()
                case pygame.K_f:
                    board_viewer.flip()


        screen.fill(Color(0,0,0))
        # updates
        board_viewer.update()
        timer_viewer.update()
        moves_viewer.update()

        screen.blit(board_viewer.surface, BOARD_OFFSET)
        screen.blit(timer_viewer.surface, TIMER_OFFSET)
        screen.blit(moves_viewer.surface, MOVES_OFFSET)
        pygame.display.update()
        
    

if __name__ == '__main__':
    main()

