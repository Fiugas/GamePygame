import random
import pygame
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Maze:
    def __init__(self, width, height, cell_size, draw_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.draw_size = draw_size
        self.maze = np.ones((height, width), dtype=int) # Atributo que armazena a estrutura do labirinto
        self.generate_maze_dfs()
        self.add_boundaries()

    def generate_maze_dfs(self):
        """Gera um labirinto usando o algoritmo de DFS."""
        start_row, start_col = 1, 1
        end_row = random.randint(1, self.height - 2)
        end_col = self.width - 2
        self.maze[start_row][start_col] = 0
        self.maze[end_row][end_col] = 0
        stack = [(start_row, start_col)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        while stack:
            current_row, current_col = stack[-1]
            neighbors = []
            random.shuffle(directions)  # Shuffle directions for more randomness
            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc
                if 1 <= new_row < self.height - 1 and 1 <= new_col < self.width - 1 and self.maze[new_row][new_col] == 1:
                    neighbors.append((new_row, new_col))
            if neighbors:
                next_row, next_col = random.choice(neighbors)
                self.maze[next_row][next_col] = 0
                self.maze[(current_row + next_row) // 2][(current_col + next_col) // 2] = 0
                stack.append((next_row, next_col))
            else:
                stack.pop()

    def add_boundaries(self):
        """Adiciona limites ao labirinto."""
        self.maze[0, :] = 1
        self.maze[-1, :] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1

    def generate_key_position(self):
        """Gera uma posição válida para a chave no labirinto."""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.is_valid_position(x, y):
                return (x, y)

    def generate_exit_position(self):
        """Gera uma posição válida para a saída no labirinto."""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.is_valid_position(x, y):
                return (x, y)

    def is_valid_position(self, x, y):
        """Verifica se a posição não é uma parede ou obstáculo."""
        return self.maze[y, x] == 0  # Supondo que 0 representa um caminho livre
    
    def get_visible_cells(self, offset_x, offset_y, screen_width, screen_height):
        """Retorna as células visíveis com base no offset e no tamanho da tela."""
        visible_cells = []
        start_col = max(0, offset_x // self.draw_size)
        end_col = min(self.width, (offset_x + screen_width) // self.draw_size + 1)
        start_row = max(0, offset_y // self.draw_size)
        end_row = min(self.height, (offset_y + screen_height) // self.draw_size + 1)
        
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                visible_cells.append((row, col))
        
        return visible_cells

    def draw(self, surface, offset_x, offset_y, screen_width, screen_height):
        """Desenha o labirinto na tela com um offset, desenhando apenas as células visíveis."""
        visible_cells = self.get_visible_cells(offset_x, offset_y, screen_width, screen_height)
        
        for row_index, col_index in visible_cells:
            if row_index == 1 and col_index == 1:
                color = GREEN  # Cor do ponto inicial
            elif col_index == self.width - 2 and self.maze[row_index][col_index] == 0:
                color = BLUE  # Cor do ponto final
            else:
                color = WHITE if self.maze[row_index][col_index] == 0 else BLACK
            pygame.draw.rect(surface, color, (col_index * self.draw_size - offset_x, row_index * self.draw_size - offset_y, self.draw_size, self.draw_size))
    ...