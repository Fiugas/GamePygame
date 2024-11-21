from states.state import State
from states.resolution_screen import ResolutionScreen
from states.sound_screen import ConfigureSound

class PauseScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: 'Exit to menu', 1: 'Change resolution', 2: 'Configure Sound', 3: 'Exit game'}
        self.menu_cursor = 0
        self.is_text_hidden = False
        self.set_blink_timer()

    def update(self, dt, player_actions):
        self.update_cursor(player_actions)
        if player_actions['PAUSE']:
                self.exit_state()
        if player_actions['SELECT']:
            selected_option = self.menu_options[self.menu_cursor]
            self.handle_selected_option(selected_option)
        self.game.reset_player_actions()

    def handle_selected_option(self, option):
        if option == 'Exit to menu':
            self.exit_state()
            self.exit_state()
        if option == 'Change resolution':
            new_state = ResolutionScreen(self.game)
            new_state.enter_state()
        if option == 'Configure Sound':
            new_state = ConfigureSound(self.game)
            new_state.enter_state()
        if option == 'Exit game':
            self.game.running, self.game.playing = False, False
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Game paused', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, 'Press ESC to resume', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, 'Exit to menu', self.game.colors['GRAY'] if self.menu_cursor != 0 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, 'Change resolution', self.game.colors['GRAY'] if self.menu_cursor != 1 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 60))
        self.game.draw_text(surface, 'Configure Sound', self.game.colors['GRAY'] if self.menu_cursor != 2 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 80))
        self.game.draw_text(surface, 'Exit game', self.game.colors['GRAY'] if self.menu_cursor != 3 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 100))