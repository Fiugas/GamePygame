import pygame
import random
from player import Player
from maze import Maze
from assets import draw_start_screen, draw_pause_screen, draw_menu_screen, draw_victory_screen
#from shaders.crt_shader import Shader


pygame.init()

# Definindo as cores
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensões da tela
WIDTH, HEIGHT = 1500, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Dimensões das células do labirinto
cell_size = 35  # Tamanho das células no labirinto
draw_size = 100  # Tamanho usado para desenhar o jogador e a tela

# Dimensões do labirinto
maze_width = WIDTH // cell_size
maze_height = HEIGHT // cell_size

# Cria o labirinto
maze = Maze(maze_width, maze_height, cell_size, draw_size)

# Função para gerar uma posição válida para a chave
def generate_key_position(maze):
    while True:
        x = random.randint(0, maze.width - 1)
        y = random.randint(0, maze.height - 1)
        if maze.is_valid_position(x, y):
            return (x, y)

# Inicializa a posição da chave
key_pos = generate_key_position(maze)

# Define a posição da chave
#key_pos = (random.randint(1, maze_height - 2), random.randint(1, maze_width - 2))
#while maze.maze[key_pos[0]][key_pos[1]] == 1:
    # key_pos = (random.randint(1, maze_height - 2), random.randint(1, maze_width - 2))

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

# Estados do jogo
START, PLAYING, PAUSED, MENU, VICTORY = "start", "playing", "paused", "menu", "victory"
game_state = START

# Inicializa o shader
#shader = Shader(game=screen)

# Loop principal do jogo
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if game_state == START:
                game_state = MENU
            elif game_state == MENU:
                if event.key == pygame.K_1:
                    game_state = PLAYING
                elif event.key == pygame.K_2:
                    run = False
            elif game_state == PLAYING:
                if event.key == pygame.K_p:
                    game_state = PAUSED
                elif event.key == pygame.K_w:
                    player.move('up', maze.maze)
                elif event.key == pygame.K_s:
                    player.move('down', maze.maze)
                elif event.key == pygame.K_a:
                    player.move('left', maze.maze)
                elif event.key == pygame.K_d:
                    player.move('right', maze.maze)
            elif game_state == PAUSED:
                if event.key == pygame.K_p:
                    game_state = PLAYING
            elif game_state == VICTORY:
                if event.key == pygame.K_RETURN:
                    game_state = MENU

    if game_state == START:
        draw_start_screen(screen, WIDTH, HEIGHT)
    elif game_state == MENU:
        draw_menu_screen(screen, WIDTH, HEIGHT)
    elif game_state == PLAYING:   
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

        # Adiciona instruções de depuração
        '''print(f"Player position: ({int(player.x + 0.5)}, {int(player.y + 0.5)})")
        print(f"Key position: {key_pos}")
        print(f"Has key: {has_key}")
        print(f"Exit position: ({maze_height - 2}, {maze_width - 2})")'''

        # Verifica se o jogador chegou à saída e tem a chave
        if (int(player.x + 0.5), int(player.y + 0.5)) == (maze_height - 2, maze_width - 2) and has_key:
            game_state = VICTORY

        # Controla a taxa de quadros
        clock.tick(60)

    elif game_state == PAUSED:
        draw_pause_screen(screen, WIDTH, HEIGHT)
    elif game_state == VICTORY:
        draw_victory_screen(screen, WIDTH, HEIGHT)

    # Aplica o shader
    #shader.render()


pygame.quit()