import pygame
import math

class Camera:
    def __init__(self, maze, view_range=3):
        self.maze = maze
        self.view_range = view_range
        self.fog_surface = None
        self.offset_x = 0
        self.offset_y = 0
        self.create_fog_surface()

    def update(self, player_x, player_y):
        center_x = pygame.display.get_surface().get_width() // (2.9 * self.maze.cell_size)
        center_y = pygame.display.get_surface().get_height() // (2.9 * self.maze.cell_size)
        self.offset_x = player_x - center_x
        self.offset_y = player_y - center_y

    def create_fog_surface(self):
        max_radius = int(self.view_range * self.maze.cell_size)
        self.fog_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        self.fog_surface.fill((0, 0, 0, 250))

    def apply_fog(self, surface, player_x, player_y):
        self.fog_surface.fill((0, 0, 0, 200))
        max_radius = int(self.view_range * self.maze.cell_size)
        fog_clear = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        for r in range(max_radius, 0, -1):
            alpha = int(255 * (r / max_radius) ** 2)
            pygame.draw.circle(fog_clear, (0, 0, 0, 255 - alpha), (max_radius, max_radius), r)
        clear_rect = fog_clear.get_rect(center=(player_x * self.maze.cell_size, player_y * self.maze.cell_size))
        self.fog_surface.blit(fog_clear, clear_rect, special_flags=pygame.BLEND_RGBA_SUB)
        surface.blit(self.fog_surface, (0, 0))

    def apply(self, x, y):
        return (x - self.offset_x) * self.maze.cell_size, (y - self.offset_y) * self.maze.cell_size
    
    def update_maze(self, maze):
        self.maze = maze
        self.create_fog_surface()

    def is_in_view_range(self, x, y, player_x, player_y):
    # Calcula a distância entre o ponto e a posição do jogador
        distance = math.sqrt((x - player_x)**2 + (y - player_y)**2)
        return distance <= self.view_range  