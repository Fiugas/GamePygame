import pygame
from states.state import State

class ResolutionScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: 'Fullscreen', 1: '1920x1080', 2: '1280x720', 3: '1024x768', 4: 'Back'}
        self.menu_cursor = 0
    
    def update(self, dt, player_actions):
        self.update_cursor(player_actions)
        if player_actions['SELECT']:
            selected_option = self.menu_options[self.menu_cursor]
            self.handle_selected_option(selected_option)
        self.game.reset_player_actions()

    def handle_selected_option(self, option):
        if option == 'Fullscreen':
            self.handle_fullscreen_option()
        if option == '1920x1080':
            self.handle_resolution_option(1920, 1080)
        if option == '1280x720':
            self.handle_resolution_option(1280, 720)
        if option == '1024x768':
            self.handle_resolution_option(1024, 768)
        if option == 'Back':
            self.exit_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Change resolution', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, 'Fullscreen', self.game.colors['GRAY'] if self.menu_cursor != 0 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, '1920x1080', self.game.colors['GRAY'] if self.menu_cursor != 1 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, '1280x720', self.game.colors['GRAY'] if self.menu_cursor != 2 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, '1024x768', self.game.colors['GRAY'] if self.menu_cursor != 3 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 60))
        self.game.draw_text(surface, 'Back', self.game.colors['GRAY'] if self.menu_cursor != 4 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 80))

    def handle_fullscreen_option(self):
        self.game.SCREEN_SIZE = self.game.NATIVE_SCREEN_SIZE
        self.game.screen = pygame.display.set_mode(self.game.SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

    def handle_resolution_option(self, width, height):
        self.game.SCREEN_SIZE = (width, height)
        self.game.screen = pygame.display.set_mode(self.game.SCREEN_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)
