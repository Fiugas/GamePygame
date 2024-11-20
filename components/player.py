import pygame
from components.collision import collision
class Player:
    def __init__(self, maze, game):
        # Inicializa o player na posição inicial do labirinto
        self.x = maze.start[0]  # Posição X inicial
        self.y = maze.start[1]  # Posição Y inicial
        self.game = game
        self.collision = collision(maze.key, maze.exit)


    def update(self, player_actions, maze):
        # Calcular novos movimentos usando dt para movimento consistente
        if player_actions['UP'] and not maze.is_wall(self.x, self.y - 1):
            self.y -= 1
        if player_actions['DOWN'] and not maze.is_wall(self.x, self.y + 1):
            self.y += 1
        if player_actions['LEFT'] and not maze.is_wall(self.x - 1, self.y):
            self.x -= 1
        if player_actions['RIGHT'] and not maze.is_wall(self.x + 1, self.y):
            self.x += 1
        self.collision.check_key_collision(self.x, self.y)

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