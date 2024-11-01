import pygame
from states.state import State

class ResolutionScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['ONE']:
            self.handle_fullscreen_option()
        if player_actions['TWO']:
            self.handle_resolution_option(1920, 1080)
        if player_actions['THREE']:
            self.handle_resolution_option(1280, 720)
        if player_actions['FOUR']:
            self.handle_resolution_option(1024, 768)
        if player_actions['FIVE']:
            self.exit_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.fill(self.game.colors['BLACK'])
        self.game.draw_text(surface, 'Change resolution', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, '1. Tela cheia', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, '2. 1920x1080', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, '3. 1280x720', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, '4. 1024x768', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 60))
        self.game.draw_text(surface, '5. Back', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 80))

    def handle_fullscreen_option(self):
        self.game.SCREEN_SIZE = self.game.NATIVE_SCREEN_SIZE
        self.game.screen = pygame.display.set_mode(self.game.SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

    def handle_resolution_option(self, width, height):
        self.game.SCREEN_SIZE = (width, height)
        self.game.screen = pygame.display.set_mode(self.game.SCREEN_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)