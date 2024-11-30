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

    def render(self, surface, cell_size, game, camera=None, visibility_check=None, player=None):
        if not self.collected:
            if camera:
                key_screen_x, key_screen_y = camera.apply(self.position[0], self.position[1])
            else:
                key_screen_x = self.position[0] * cell_size
                key_screen_y = self.position[1] * cell_size
            # Render key and exit if in view range
            if visibility_check is None or visibility_check(self.position[0], self.position[1], player.x, player.y):
                surface.blit(pygame.transform.scale(game.key, (cell_size, cell_size)), (key_screen_x, key_screen_y))