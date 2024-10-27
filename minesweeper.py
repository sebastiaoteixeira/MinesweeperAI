import random

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.mines = set()
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.generate_board()
    
    def generate_board(self):
        for _ in range(self.mines_count):
            row, col = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            while self.board[row][col] == -1:
                row, col = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            self.board[row][col] = -1
            self.mines.add((col, row))
            for i in range(row-1, row+2):
                for j in range(col-1, col+2):
                    if 0 <= i < self.rows and 0 <= j < self.cols and self.board[i][j] != -1:
                        self.board[i][j] += 1

    def __getitem__(self, key):
        return self.board[key]

    
    @property
    def size(self):
        return self.rows, self.cols

    @property
    def area(self):
        return self.rows * self.cols
    
    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])


class Game:
    def __init__(self, rows, cols, mines):
        self.map = Board(rows, cols, mines)
        self.revealed = set()
        self.flags = set()
        self.win = False
        self.lose = False
    
    @property
    def over(self):
        return self.win or self.lose
    

    def _reveal_cells(self, x, y):
        self.revealed.add((x, y))
        if self.map[y][x] == 0:
            for i in range(max(0, x-1), min(self.map.size[1], x+2)):
                for j in range(max(0, y-1), min(self.map.size[0], y+2)):
                    if (i, j) not in self.revealed:
                        self._reveal_cells(i, j)
    
    def reveal_cells(self, x, y):
        if (x, y) not in self.revealed and (x, y) not in self.flags:
            self._reveal_cells(x, y)
            if self.map[y][x] == -1:
                self.lose = True
                print('Game Over!')
        
        if len(self.revealed) == self.map.area - self.map.mines_count:
            self.win = True
            for (x, y) in self.map.mines:
                if (x, y) not in self.flags:
                    self.flags.add((x, y))
    
    def toggle_flag(self, x, y):
        if (x, y) in self.flags:
            self.flags.remove((x, y))
        else:
            self.flags.add((x, y))
    
    @property
    def state(self):
        return {
            'map': [[self.map[y][x] if (x, y) in self.revealed else (-2 if (x, y) in self.flags else -3) for x in range(self.map.size[1])] for y in range(self.map.size[0])],
            'win': self.win,
            'lose': self.lose,
            'over': self.over,
            'flags': len(self.flags),
            'mines': self.map.mines_count,
            'revealed': len(self.revealed),
            'area': self.map.area
        }