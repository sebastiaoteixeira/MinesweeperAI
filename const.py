from enum import Enum

class Actions(Enum):
    REVEAL = 1
    FLAG = 2
    QUIT = 3
    RESTART = 4

# Definindo constantes do jogo
CELL_SIZE = 40
NUM_CELLS_X = 24
NUM_CELLS_Y = 24
WINDOW_HEIGHT = CELL_SIZE * NUM_CELLS_Y
WINDOW_WIDTH = CELL_SIZE * NUM_CELLS_X
NUM_MINES = 80

# Cores
BACKGROUND_COLOR = (189, 189, 189)
BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)
FLAG_COLOR = (255, 0, 0)
COR_MINA = (0, 0, 0)