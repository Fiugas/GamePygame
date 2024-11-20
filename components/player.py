import pygame
class Player:
    def __init__(self, maze):
        # Inicializa o player na posição inicial do labirinto
        self.x = maze.start[0]  # Posição X inicial
        self.y = maze.start[1]  # Posição Y inicial


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
        # Você pode usar um sprite ou simplesmente desenhar um retângulo
        pygame.draw.rect(surface, game.colors['RED'], player_rect)  # Vermelho para o player
