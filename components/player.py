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
        self.move_player(player_actions, maze)

    def move_player(self, player_actions, maze):
        movements = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        for action, (dx, dy) in movements.items():
            if player_actions[action] and not self.collision.check_wall_collision(self.x + dx, self.y + dy, maze):
                self.x += dx
                self.y += dy

    def render(self, surface, cell_size, game, camera=None):
        # Use camera's apply method if provided
        self.start_player(surface, cell_size, game, camera)
        

    def start_player(self, surface, cell_size, game, camera=None):
        # Desenha o player
        screen_x = self.x * cell_size
        screen_y = self.y * cell_size
        
        if camera:
            screen_x, screen_y = camera.apply(self.x, self.y)
        
        # Render player
        surface.blit(pygame.transform.scale(game.player, (cell_size, cell_size)),pygame.Rect(screen_x, screen_y, cell_size, cell_size))

    def update_maze(self, maze):
        self.collision = collision(maze.key, maze.exit)
        self.x = maze.start[0]
        self.y = maze.start[1]