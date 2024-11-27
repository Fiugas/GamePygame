import pygame

class Entity:
    def __init__(self, position):
        self.position = position

class Key(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.collected = False

    def collect(self):
        self.collected = True

    def render(self, surface, cell_size, game):
        if not self.collected:
            rect = pygame.Rect(self.position[0] * cell_size, self.position[1] * cell_size, cell_size, cell_size)
            surface.blit(pygame.transform.scale(game.key, (cell_size, cell_size)), rect)