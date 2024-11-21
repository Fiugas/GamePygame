import pygame
from states.state import State

class ConfigureSound(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: 'Volume', 1: 'Change Music', 2: 'Back'}
        self.menu_cursor = 0
        self.volume = 0.5  # Default volume at 50%
    
    def update(self, dt, player_actions):
        self.update_cursor(player_actions)
        if player_actions['LEFT']:
            self.volume = max(0.0, self.volume - 0.1)
        if player_actions['RIGHT']:
            self.volume = min(1.0, self.volume + 0.1)
        self.game.adjust_volume(self.volume)
        if player_actions['SELECT']:
            selected_option = self.menu_options[self.menu_cursor]
            self.handle_selected_option(selected_option)
        self.game.reset_player_actions()

    def handle_selected_option(self, option):
        if option == 'Change Music':
            self.game.change_music()
        if option == 'Back':
            self.exit_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Configure Sound', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        # Volume text with current volume percentage
        volume_text = f'Volume: {int(self.volume * 100)}%'
        self.game.draw_text(surface, volume_text,self.game.colors['WHITE'] if self.menu_cursor == 0 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, 'Change Music', self.game.colors['WHITE'] if self.menu_cursor == 1 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, 'Back', self.game.colors['WHITE'] if self.menu_cursor == 2 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))