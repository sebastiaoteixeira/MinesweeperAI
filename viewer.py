import pygame
import sys
from minesweeper import Game
from const import *

ai_mode = False

# Inicializa o Pygame
pygame.init()

# Font
font = pygame.font.SysFont(None, 36)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, BORDER_COLOR, rect, 1)

colors = [BACKGROUND_COLOR, (0, 255, 0), (255, 255, 0), (255, 165, 0), (255, 0, 0), (128, 0, 128), (0, 0, 255), (0, 255, 255)]

def draw_board(game):
    for y in range(NUM_CELLS_Y):
        for x in range(NUM_CELLS_X):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) in game.revealed:
                if game.map[y][x] == -1:
                    pygame.draw.rect(window, COR_MINA, rect)  # Mine
                else:
                    pygame.draw.rect(window, colors[game.map[y][x]], rect)  # Revealed cell
                    if game.map[y][x] >= 0:
                        texto = font.render(str(game.map[y][x]), True, TEXT_COLOR)
                        window.blit(texto, (x * CELL_SIZE + 10, y * CELL_SIZE))
            elif (x, y) in game.flags:
                pygame.draw.rect(window, BACKGROUND_COLOR, rect)
                # draw a vertical line
                pygame.draw.line(window, FLAG_COLOR, (x * CELL_SIZE + 10, y * CELL_SIZE + 5), (x * CELL_SIZE + 10, y * CELL_SIZE + 30), 3)
                # draw a triangle
                pygame.draw.polygon(window, FLAG_COLOR, [(x * CELL_SIZE + 10, y * CELL_SIZE + 5), (x * CELL_SIZE + 30, y * CELL_SIZE + 13), (x * CELL_SIZE + 10, y * CELL_SIZE + 20)])
            else:
                # Célula oculta
                pygame.draw.rect(window, BACKGROUND_COLOR, rect)

            pygame.draw.rect(window, BORDER_COLOR, rect, 1)


# Função principal do jogo
def loop(executor):
    game = Game(NUM_CELLS_Y, NUM_CELLS_X, NUM_MINES)
    
    while True:
        action, x, y = executor.exec(game.state)
        print(action, x, y)
        if action == Actions.REVEAL:
            game.reveal_cells(x, y)
        elif action == Actions.FLAG:
            game.toggle_flag(x, y)
        elif action == Actions.QUIT:
            pygame.quit()
            sys.exit()
        elif action == Actions.RESTART:
            game = Game(NUM_CELLS_Y, NUM_CELLS_X, NUM_MINES)

        # Desenha o jogo
        window.fill(BACKGROUND_COLOR)
        draw_board(game)
        draw_grid()

        # Se o jogo terminou, desenha uma mensagem
        if game.lose:
            texto_game_over = font.render("Game Over!", True, TEXT_COLOR)
            window.blit(texto_game_over, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20))
        elif game.win:
            texto_vitoria = font.render("Você venceu!", True, TEXT_COLOR)
            window.blit(texto_vitoria, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20))

        pygame.display.update()

        # Espera um tempo
        if ai_mode:
            pygame.time.wait(100)
