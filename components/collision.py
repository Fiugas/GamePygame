import pygame
class collision:
    def __init__(self, key, exit):
        self.key = key
        self.exit = exit

    def check_wall_collision(self, x, y, maze):
        # First check if the position is within valid maze boundaries
        if not maze.is_valid_position(x, y):
            return True  # Treat out-of-bounds positions as walls
        # Then check if the position is a wall
        return maze.is_wall(x, y)

    def check_key_collision(self, x, y):
        if x == self.key.position[0] and y == self.key.position[1]:
            self.key.collect()


    def check_exit_collision(self, player_position):
        return player_position == self.exit