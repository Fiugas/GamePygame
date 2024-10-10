import pygame

RED = (255, 0, 0)

class Player:
    def __init__(self, x, y, draw_size):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.draw_size = draw_size

    def move(self, direction, maze):
        if direction == 'up' and maze[self.target_y - 1][self.target_x] == 0:
            self.target_y -= 1
        elif direction == 'down' and maze[self.target_y + 1][self.target_x] == 0:
            self.target_y += 1
        elif direction == 'left' and maze[self.target_y][self.target_x - 1] == 0:
            self.target_x -= 1
        elif direction == 'right' and maze[self.target_y][self.target_x + 1] == 0:
            self.target_x += 1

    def update(self):
        self.x += (self.target_x - self.x) * 0.3
        self.y += (self.target_y - self.y) * 0.3

    def draw(self, surface, offset_x, offset_y):
        pygame.draw.rect(surface, RED, (self.x * self.draw_size - offset_x, self.y * self.draw_size - offset_y, self.draw_size, self.draw_size))