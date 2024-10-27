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
            # wait for a click to restart the game
            while True:
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    return Actions.QUIT, 0, 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return Actions.RESTART, 0, 0
        for row in range(len(state['map'])):
            for cell in range(len(state['map'][row])):
                if state['map'][row][cell] == -3:
                    if self.is_free(state, row, cell):
                        return Actions.REVEAL, cell, row
        for row in range(len(state['map'])):
            for cell in range(len(state['map'][row])):
                if state['map'][row][cell] == -3:
                    if self.is_mine(state, row, cell):
                        return Actions.FLAG, cell, row
        
        #x, y = self.chooseByProbabilities(state)
        x = 0
        y = 0
        while state['map'][y][x] != -3:
            x += 1
            if x == len(state['map'][0]):
                x = 0
                y += 1
        return Actions.REVEAL, x, y
    
    def chooseByProbabilities(self, state):
        free_cells = [(x, y) for x in range(len(state['map'][0])) for y in range(len(state['map'])) if state['map'][y][x] == -3]
        free_cells.sort(key=lambda x: self.calculate_probability(state, x[1], x[0]))
        return free_cells[0]
    
    def calculate_probability(self, state, row, cell):
        probability = 0
        for i in range(max(0, row-1), min(len(state['map']), row+2)):
            for j in range(max(0, cell-1), min(len(state['map'][row]), cell+2)):
                if state['map'][i][j] > 0:
                    neighbor_flags = self.count_neighbor_flags(state, i, j)
                    neighbor_unrevealed = self.count_neighbor_unrevealed(state, i, j)
                    probability += (state['map'][i][j] - neighbor_flags) / neighbor_unrevealed
                elif probability == 0:
                    probability = (state['mines'] - state['flags']) / (state['area'] - state['revealed'])
        return probability

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
