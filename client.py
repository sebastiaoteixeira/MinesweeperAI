import pygame
import sys
from minesweeper import Game
from const import *

class human():
    def exec(self, state):
        # get element from the queue
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return Actions.QUIT, 0, 0
            
        if event.type == pygame.MOUSEBUTTONDOWN and not state.over:
            x, y = pygame.mouse.get_pos()
            cell_x = x // CELL_SIZE
            cell_y = y // CELL_SIZE
                
            # Left click to reveal cell
            if event.button == 1:
                return Actions.REVEAL, cell_x, cell_y
            # Right click to (un)place flag
            elif event.button == 3:
                return Actions.FLAG, cell_x, cell_y
        elif event.type == pygame.MOUSEBUTTONDOWN and state.over:
            return Actions.RESTART, 0, 0
        return None, 0, 0

class ai():
    def exec(self, state):
        print(state)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return Actions.QUIT, 0, 0
        
        if state['over']:
            return None, 0, 0
        for row in range(len(state['map'])):
            for cell in range(len(state['map'][row])):
                if state['map'][row][cell] == -3:
                    if self.is_certain(state, row, cell):
                        return Actions.REVEAL, row, cell
        return None, 0, 0
    
    def is_certain(self, state, row, cell):
        print(state)
        return False
    
