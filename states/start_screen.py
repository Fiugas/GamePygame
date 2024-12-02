from states.state import State
from states.title_screen import TitleScreen


class StartScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.is_text_hidden = False
        self.set_blink_timer()

    def update(self, dt, player_actions):
        if player_actions['SELECT']:
            new_state = TitleScreen(self.game)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface,'MAZECRAFT', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.blink_message(dt)
        if self.is_text_hidden:
            self.game.draw_text(surface, 'Press Enter to start', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 2))
