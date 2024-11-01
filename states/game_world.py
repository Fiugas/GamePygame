from states.state import State
from states.pause_screen import PauseScreen

class GameWorld(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['PAUSE']:
            new_state = PauseScreen(self.game)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, surface):
        surface.fill(self.game.colors['WHITE'])