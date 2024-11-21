from states.state import State
class Nextlevelscreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: 'Next level', 1: 'Exit game'}
        self.menu_cursor = 0

    def update(self, dt, player_actions):
        self.update_cursor(player_actions)
        if player_actions['SELECT']:
            selected_option = self.menu_options[self.menu_cursor]
            self.handle_selected_option(selected_option)
        self.game.reset_player_actions()

    def handle_selected_option(self, option):
        if option == 'Next level':
            self.exit_state()
        if option == 'Exit game':
            self.game.running, self.game.playing = False, False
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Victory', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, 'Next level', self.game.colors['GRAY'] if self.menu_cursor != 0 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, 'Exit game', self.game.colors['GRAY'] if self.menu_cursor != 1 else self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 80))
