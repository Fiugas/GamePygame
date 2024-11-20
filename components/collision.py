import pygame
class collision:
    def __init__(self, key, exit):
        self.key = key
        self.exit = exit

    def check_key_collision(self, x, y):
        if x == self.key.position[0] and y == self.key.position[1]:
            self.key.collect()


    def check_exit_collision(self, player_position):
        return player_position == self.exit