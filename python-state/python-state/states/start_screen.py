from states.state import State
from states.title_screen import TitleScreen

class StartScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['SELECT']:
            new_state = TitleScreen(self.game)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, surface):
        surface.fill(self.game.colors['BLACK'])
        self.game.draw_text(surface, 'Pressione Enter para começar', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 2))