from states.state import State
from states.title_screen import TitleScreen


class StartScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.hide_text = True
        self.blink_count = 0

    def update(self, dt, player_actions):
        if player_actions['SELECT']:
            new_state = TitleScreen(self.game)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface,'MAZECRAFT', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        if self.hide_text:
            self.blink_count += dt
            if self.blink_count >= 0.75:
                self.hide_text = False
                self.blink_count = 0
        else:
            self.game.draw_text(surface, 'Press Enter to start', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 2))
            self.blink_count += dt
            if self.blink_count >= 0.75:
                self.hide_text = True
                self.blink_count = 0