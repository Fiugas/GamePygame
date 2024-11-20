import pygame
class Player:
    def __init__(self, maze, game):
        # Inicializa o player na posição inicial do labirinto
        self.x = maze.start[0]  # Posição X inicial
        self.y = maze.start[1]  # Posição Y inicial
        self.game = game

    def update(self, dt, player_actions, cell_size):
        # Calcular novos movimentos usando dt para movimento consistente
        if player_actions['UP']:
            print("up")
            self.y -= (cell_size*5) * dt
        if player_actions['DOWN']:
            print("down")
            self.y += (cell_size*5) * dt
        if player_actions['LEFT']:
            print("left")
            self.x -= (cell_size*5) * dt
        if player_actions['RIGHT']:
            print("right")
            self.x += (cell_size*5) * dt

    def render(self, surface, cell_size, game):
        self.start_player(surface, cell_size, game)

    def start_player(self, surface, cell_size, game):
        # Desenha o player
        player_rect = pygame.Rect(
            self.x * cell_size,  # Posição X na tela
            self.y * cell_size,  # Posição Y na tela
            cell_size,           # Largura
            cell_size            # Altura
        )
        pygame.draw.rect(surface, game.colors['RED'], player_rect)