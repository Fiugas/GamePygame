from states.state import State
from states.resolution_screen import ResolutionScreen

class PauseScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['PAUSE']:
            self.exit_state()
        if player_actions['ONE']:
            self.exit_state()
            self.exit_state()
        if player_actions['TWO']:
            new_state = ResolutionScreen(self.game)
            new_state.enter_state()
        if player_actions['THREE']:
            self.game.running, self.game.playing = False, False
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.fill(self.game.colors['BLACK'])
        self.game.draw_text(surface, 'Game paused', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, 'Press ESC to resume', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, '1. Exit to menu', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, '2. Change resolution', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, '3. Exit game', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 60))