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
        self.collision.check_key_collision(self.x, self.y)
        # Calcular novos movimentos usando dt para movimento consistente
        if player_actions['UP'] and not self.collision.check_wall_collision(self.x, self.y - 1, maze):
            self.y -= 1
        if player_actions['DOWN'] and not self.collision.check_wall_collision(self.x, self.y + 1, maze):
            self.y += 1
        if player_actions['LEFT'] and not self.collision.check_wall_collision(self.x - 1, self.y, maze):
            self.x -= 1
        if player_actions['RIGHT'] and not self.collision.check_wall_collision(self.x + 1, self.y, maze):
            self.x += 1

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
        surface.blit(pygame.transform.scale(game.player, (cell_size, cell_size)), player_rect)

    def update_maze(self, maze):
        self.collision = collision(maze.key, maze.exit)
        self.x = maze.start[0]
        self.y = maze.start[1]