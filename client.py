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
            
        if event.type == pygame.MOUSEBUTTONDOWN and not state["over"]:
            x, y = pygame.mouse.get_pos()
            cell_x = x // CELL_SIZE
            cell_y = y // CELL_SIZE
                
            # Left click to reveal cell
            if event.button == 1:
                return Actions.REVEAL, cell_x, cell_y
            # Right click to (un)place flag
            elif event.button == 3:
                return Actions.FLAG, cell_x, cell_y
        elif event.type == pygame.MOUSEBUTTONDOWN and state["over"]:
            return Actions.RESTART, 0, 0
        return None, 0, 0


import random

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
                    if self.is_free(state, row, cell):
                        return Actions.REVEAL, cell, row
                    if self.is_mine(state, row, cell):
                        return Actions.FLAG, cell, row
        x, y = random.randint(0, len(state['map'])-1), random.randint(0, len(state['map'][0])-1)
        while state['map'][y][x] != -3:
            x, y = random.randint(0, len(state['map'])-1), random.randint(0, len(state['map'][0])-1)
        return Actions.REVEAL, x, y
    
    def is_free(self, state, row, cell):
        for i in range(max(0, row-1), min(len(state['map']), row+2)):
            for j in range(max(0, cell-1), min(len(state['map'][row]), cell+2)):
                if state['map'][i][j] > 0:
                    neighbor_flags = self.count_neighbor_flags(state, i, j)
                    if neighbor_flags == state['map'][i][j]:
                        return True
        return False
    
    def is_mine(self, state, row, cell):
        for i in range(max(0, row-1), min(len(state['map']), row+2)):
            for j in range(max(0, cell-1), min(len(state['map'][row]), cell+2)):
                if state['map'][i][j] > 0:
                    neighbor_flags = self.count_neighbor_flags(state, i, j)
                    neighbor_unrevealed = self.count_neighbor_unrevealed(state, i, j)
                    if neighbor_flags + neighbor_unrevealed == state['map'][i][j]:
                        return True
        return False
    
    def count_neighbor_unrevealed(self, state, row, cell):
        count = 0
        for i in range(max(0, row-1), min(len(state['map']), row+2)):
            for j in range(max(0, cell-1), min(len(state['map'][row]), cell+2)):
                if state['map'][i][j] == -3:
                    count += 1
        return count

    def count_neighbor_flags(self, state, row, cell):
        count = 0
        for i in range(max(0, row-1), min(len(state['map']), row+2)):
            for j in range(max(0, cell-1), min(len(state['map'][row]), cell+2)):
                if state['map'][i][j] == -2:
                    count += 1
        return count
