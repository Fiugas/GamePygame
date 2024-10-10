import pygame
import random
from maze import Maze
from player import Player

pygame.init()

# Definindo as cores
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensões da tela
WIDTH, HEIGHT = 1500, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Dimensões das células do labirinto
cell_size = 50  # Tamanho das células no labirinto
draw_size = 100  # Tamanho usado para desenhar o jogador e a tela

# Dimensões do labirinto
maze_width = WIDTH // cell_size
maze_height = HEIGHT // cell_size

# Cria o labirinto
maze = Maze(maze_width, maze_height, cell_size, draw_size)

# Define a posição da chave
key_pos = (random.randint(1, maze_height - 2), random.randint(1, maze_width - 2))
while maze.maze[key_pos[0]][key_pos[1]] == 1:
    key_pos = (random.randint(1, maze_height - 2), random.randint(1, maze_width - 2))

# Cria o jogador
player = Player(1, 1, draw_size)
has_key = False  # Variável para rastrear se a chave foi coletada

def draw_key(surface, key_pos, offset_x, offset_y):
    """Desenha a chave na tela."""
    key_x, key_y = key_pos
    pygame.draw.rect(surface, YELLOW, (key_x * draw_size - offset_x, key_y * draw_size - offset_y, draw_size, draw_size))

def show_victory_screen():
    """Mostra a tela de vitória."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Você venceu!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Configura o relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Loop principal do jogo
run = True
while run:
    screen.fill(BLACK)
    
    # Calcula o offset da câmera
    offset_x = player.x * draw_size - WIDTH // 2 + draw_size // 2
    offset_y = player.y * draw_size - HEIGHT // 2 + draw_size // 2
    
    maze.draw(screen, offset_x, offset_y)
    if not has_key:
        draw_key(screen, key_pos, offset_x, offset_y)
    player.draw(screen, offset_x, offset_y)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move('up', maze.maze)
            elif event.key == pygame.K_s:
                player.move('down', maze.maze)
            elif event.key == pygame.K_a:
                player.move('left', maze.maze)
            elif event.key == pygame.K_d:
                player.move('right', maze.maze)

    player.update()

    # Verifica se o jogador coletou a chave
    if (int(player.x + 0.5), int(player.y + 0.5)) == key_pos:
        has_key = True

    # Verifica se o jogador chegou à saída e tem a chave
    if (int(player.x + 0.5), int(player.y + 0.5)) == (maze_height - 2, maze_width - 2) and has_key:
        show_victory_screen()
        run = False

    # Controla a taxa de quadros
    clock.tick(60)

pygame.quit()