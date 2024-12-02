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

    def update(self, player):
        center_x = pygame.display.get_surface().get_width() // (2.9 * self.maze.cell_size)
        center_y = pygame.display.get_surface().get_height() // (2.9 * self.maze.cell_size)
        self.offset_x = player.x - center_x
        self.offset_y = player.y - center_y

    def create_fog_surface(self):
        max_radius = int( 5 * self.maze.cell_size)
        self.fog_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)

    def apply_fog(self, surface, player):
        screen_width, screen_height = surface.get_size()
        self.fog_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.fog_surface.fill((0, 0, 0, 215))
        max_radius = int(self.view_range * self.maze.cell_size)
        fog_clear = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        for r in range(max_radius, 0, -1):
            alpha = int(255 * (r / max_radius) ** 2)
            pygame.draw.circle(fog_clear, (0, 0, 0, 255 - alpha), (max_radius, max_radius), r)
        player_screen_x = (player.x - self.offset_x) * self.maze.cell_size
        player_screen_y = (player.y - self.offset_y) * self.maze.cell_size

        clear_rect = fog_clear.get_rect(center=(player_screen_x, player_screen_y))
        self.fog_surface.blit(fog_clear, clear_rect, special_flags=pygame.BLEND_RGBA_SUB)
        surface.blit(self.fog_surface, (0, 0))

    def apply(self, x, y):
        return (x - self.offset_x) * self.maze.cell_size, (y - self.offset_y) * self.maze.cell_size

    def update_maze(self, maze):
        self.maze = maze
        self.create_fog_surface()

    def is_in_view_range(self, x, y, player):
        distance = math.sqrt((x - player.x)**2 + (y - player.y)**2)
        view_distance = min(self.view_range * self.maze.cell_size, distance)
        distance_cells = int(distance / self.maze.cell_size)
        return distance_cells <= view_distance